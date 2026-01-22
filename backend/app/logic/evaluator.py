from __future__ import annotations

import re
from typing import Any

from fastapi import HTTPException
from simpleeval import SimpleEval

from ..domain.models import Engine, ModuleDef, QuestionDef


class Evaluator:
    def __init__(self) -> None:
        self._contains_pattern = re.compile(r"([A-Za-z0-9_.\-]+)\s+contains\s+('.*?'|\".*?\"|[A-Za-z0-9_.\-]+)")

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
        for q in module.questions:
            if not self.question_visible(q, answers, params):
                continue
            if q.id not in answers:
                visible = [q.raw]
                break
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
        evaluator.names = self._build_env(answers, params)
        try:
            normalized = self._normalize_expr(self._rewrite_contains(expr))
            return bool(evaluator.eval(normalized))
        except Exception:
            return False

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

    def _build_env(self, answers: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        env: dict[str, Any] = {}
        for key, value in {**params, **answers}.items():
            env[self._normalize_name(key)] = value
        return env

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
