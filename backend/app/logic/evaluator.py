from __future__ import annotations

import re
from typing import Any

from fastapi import HTTPException
from simpleeval import AttributeDoesNotExist, NameNotDefined, SimpleEval

from ..domain.models import Engine, ModuleDef, QuestionDef


class Evaluator:
    def __init__(self) -> None:
        self._contains_pattern = re.compile(r"([A-Za-z0-9_.\-]+)\s+contains\s+('.*?'|\".*?\"|[A-Za-z0-9_.\-]+)")
        self._template_pattern = re.compile(r"\{\{\s*([A-Za-z0-9_.\-]+)\s*\}\}")

    def validate_answer(self, question: QuestionDef, value: Any) -> Any:
        if question.qtype == "boolean":
            if isinstance(value, bool):
                return value
            raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "expected": "boolean"})
        if question.qtype == "single_choice":
            options = question.options or []
            allowed = {opt.get("value") for opt in options}
            if value not in allowed:
                raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "value": value})
            return value
        if question.qtype in {"multi_choice", "multiple_choice"}:
            if not isinstance(value, list):
                raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "expected": "list"})
            if len(set(value)) != len(value):
                raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "duplicates": True})
            options = question.options or []
            allowed = {opt.get("value") for opt in options}
            invalid = [v for v in value if v not in allowed]
            if invalid:
                raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "invalid": invalid})
            exclusives = {opt.get("value") for opt in options if opt.get("exclusive")}
            if exclusives and any(v in exclusives for v in value):
                if len(value) != 1:
                    raise HTTPException(status_code=400, detail={"invalid_answer": question.id, "exclusive": True})
            return value
        return value

    def question_visible(self, question: QuestionDef, answers: dict[str, Any], params: dict[str, Any]) -> bool:
        if not question.dependency:
            return True
        return self.eval_condition(question.dependency, answers, params)

    def module_payload(self, module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        visible: list[dict[str, Any]] = []
        last_answered: dict[str, Any] | None = None
        last_visible: dict[str, Any] | None = None
        for q in module.questions:
            if not self.question_visible(q, answers, params):
                continue
            last_visible = q.raw
            if q.id not in answers:
                visible = [q.raw]
                break
            last_answered = q.raw
        if not visible:
            if last_answered is not None:
                visible = [last_answered]
            elif last_visible is not None:
                visible = [last_visible]
        return {
            "id": module.module_id,
            "title": module.title,
            "description": module.description,
            "questions": visible,
        }

    def module_complete(self, module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> bool:
        for q in module.questions:
            if self.question_visible(q, answers, params) and q.id not in answers:
                return False
        return True

    def prune_hidden_answers(self, module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> bool:
        removed = False
        for q in module.questions:
            if q.id in answers and not self.question_visible(q, answers, params):
                del answers[q.id]
                removed = True
        return removed

    def next_action(self, module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> tuple[str, str | None, str | None]:
        module_done = self.module_complete(module, answers, params)
        params_with_flag = {**params, "Module_finished": module_done}
        for rule in module.router:
            if rule.condition and not self.eval_condition(rule.condition, answers, params_with_flag):
                continue
            action_lower = (rule.action or "").lower()
            if action_lower in {"jump", "next"}:
                if not rule.target_module_id:
                    raise HTTPException(status_code=500, detail={"router_target_missing": rule.action})
                return ("module", rule.target_module_id, rule.message)
            if action_lower in {"terminate", "end", "finish"}:
                return ("result", None, rule.message)
        return ("module", module.module_id, None)

    def compute_parameters(self, engine: Engine, answers: dict[str, Any]) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for module in engine.modules:
            for variable in module.variables:
                value = (
                    variable.initial_value
                    if variable.initial_value is not None
                    else self._default_for_type(variable.var_type)
                )
                if (variable.var_type or "").lower() in {"string_list", "list"}:
                    collected: list[Any] = []
                    else_value: Any | None = None
                    for rule in variable.rules:
                        if rule.condition.strip().lower() == "else":
                            else_value = rule.value
                            continue
                        if self.eval_condition(rule.condition, answers, params):
                            collected.append(rule.value)
                    if collected:
                        value = collected
                    elif else_value is not None:
                        value = else_value if isinstance(else_value, list) else [else_value]
                else:
                    for rule in variable.rules:
                        if self.eval_condition(rule.condition, answers, params):
                            value = rule.value
                            break
                params[variable.name] = value
        for key in list(params.keys()):
            params[key] = self._render_template(params[key], answers, params)
        return params

    def compute_conclusion(self, params: dict[str, Any]) -> dict[str, Any] | None:
        return {
            "Role": params.get("Role"),
            "Type": params.get("Type"),
            "Risk_level": params.get("Risk_level"),
            "View": params.get("View"),
        }

    def eval_condition(self, expr: str, answers: dict[str, Any], params: dict[str, Any]) -> bool:
        if not expr:
            return True
        if expr.strip().lower() == "else":
            return True
        evaluator = SimpleEval()
        normalized = self._normalize_expr(self._rewrite_contains(self._rewrite_in_list(expr)))
        env = self._build_env(answers, params)
        keywords = {"and", "or", "not", "in", "is", "True", "False", "None"}
        for name in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", normalized):
            if name in keywords:
                continue
            if name not in env:
                env[name] = None
        evaluator.names = env
        try:
            return bool(evaluator.eval(normalized))
        except (NameNotDefined, AttributeDoesNotExist, TypeError):
            return False
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail={"invalid_condition": expr, "error": str(exc)},
            )

    def _normalize_name(self, name: str) -> str:
        normalized = re.sub(r"[^0-9A-Za-z_]", "_", name)
        if normalized and normalized[0].isdigit():
            normalized = f"_{normalized}"
        return normalized

    def _normalize_expr(self, expr: str) -> str:
        out: list[str] = []
        i = 0
        length = len(expr)
        keywords = {"and", "or", "not", "in", "is", "True", "False", "None", "contains"}
        while i < length:
            ch = expr[i]
            if ch in "\"'":
                quote = ch
                out.append(ch)
                i += 1
                while i < length and expr[i] != quote:
                    out.append(expr[i])
                    i += 1
                if i < length:
                    out.append(expr[i])
                    i += 1
                continue
            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < length and (expr[i].isalnum() or expr[i] in "._-"):
                    i += 1
                token = expr[start:i]
                if token in keywords:
                    out.append(token)
                else:
                    out.append(self._normalize_name(token))
                continue
            out.append(ch)
            i += 1
        return "".join(out)

    def _rewrite_contains(self, expr: str) -> str:
        prev = expr
        while True:
            updated = self._contains_pattern.sub(r"\2 in \1", prev)
            if updated == prev:
                return updated
            prev = updated

    def _rewrite_in_list(self, expr: str) -> str:
        out: list[str] = []
        i = 0
        length = len(expr)
        while i < length:
            ch = expr[i]
            if ch in "\"'":
                quote = ch
                out.append(ch)
                i += 1
                while i < length and expr[i] != quote:
                    out.append(expr[i])
                    i += 1
                if i < length:
                    out.append(expr[i])
                    i += 1
                continue
            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < length and (expr[i].isalnum() or expr[i] in "._-"):
                    i += 1
                token = expr[start:i]
                j = i
                while j < length and expr[j].isspace():
                    j += 1
                if expr[j:j + 2] == "in" and (j + 2 == length or not expr[j + 2].isalnum()):
                    k = j + 2
                    while k < length and expr[k].isspace():
                        k += 1
                    if k < length and expr[k] == "[":
                        k += 1
                        list_start = k
                        quote = None
                        while k < length:
                            current = expr[k]
                            if quote:
                                if current == quote:
                                    quote = None
                                k += 1
                                continue
                            if current in "\"'":
                                quote = current
                                k += 1
                                continue
                            if current == "]":
                                break
                            k += 1
                        if k < length and expr[k] == "]":
                            list_str = expr[list_start:k]
                            items: list[str] = []
                            current = ""
                            quote = None
                            for ch_item in list_str:
                                if quote:
                                    current += ch_item
                                    if ch_item == quote:
                                        quote = None
                                    continue
                                if ch_item in "\"'":
                                    quote = ch_item
                                    current += ch_item
                                    continue
                                if ch_item == ",":
                                    if current.strip():
                                        items.append(current.strip())
                                    current = ""
                                    continue
                                current += ch_item
                            if current.strip():
                                items.append(current.strip())
                            if items:
                                out.append("(" + " or ".join(f"{token} == {item}" for item in items) + ")")
                                i = k + 1
                                continue
                out.append(token)
                continue
            out.append(ch)
            i += 1
        return "".join(out)

    def _build_env(self, answers: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        env: dict[str, Any] = {}
        for key, value in {**params, **answers}.items():
            env[self._normalize_name(key)] = value
        return env

    def _render_template(self, value: Any, answers: dict[str, Any], params: dict[str, Any]) -> Any:
        if isinstance(value, str):
            return self._template_pattern.sub(
                lambda match: self._stringify_placeholder(match.group(1), answers, params),
                value,
            )
        if isinstance(value, list):
            return [self._render_template(item, answers, params) for item in value]
        return value

    def _stringify_placeholder(self, name: str, answers: dict[str, Any], params: dict[str, Any]) -> str:
        if name in params:
            raw = params[name]
        elif name in answers:
            raw = answers[name]
        else:
            raw = None
        if raw is None:
            return ""
        if isinstance(raw, list):
            return "; ".join(str(item) for item in raw if item is not None)
        return str(raw)

    @staticmethod
    def _default_for_type(param_type: str | None) -> Any:
        if param_type is None:
            return None
        lower = param_type.lower()
        if lower == "boolean":
            return False
        if lower == "string":
            return ""
        if lower in {"string_list", "list"}:
            return []
        return None
