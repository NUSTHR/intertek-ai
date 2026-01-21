from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import yaml

AnswerValue = Any


@dataclass
class QuestionDef:
    id: str
    qtype: str
    dependency: str | None
    options: list[dict[str, Any]] | None
    raw: dict[str, Any]


@dataclass
class ParameterUpdateDef:
    parameter: str
    param_type: str | None
    logic: str
    compiled: Any


@dataclass
class RouterRuleDef:
    condition: str
    compiled: Any
    action: str
    message: str | None


@dataclass
class ModuleDef:
    module_id: str
    module_code: str
    title: str
    description: str | None
    questions: list[QuestionDef]
    questions_by_id: dict[str, QuestionDef]
    parameter_updates: list[ParameterUpdateDef]
    router: list[RouterRuleDef]


@dataclass
class Engine:
    modules: list[ModuleDef]
    modules_by_id: dict[str, ModuleDef]
    modules_by_code: dict[str, ModuleDef]


@dataclass
class Session:
    id: str
    answers: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    current_module_id: str | None = None


class InitResponse(BaseModel):
    session_id: str
    module: dict[str, Any]


class ModuleResponse(BaseModel):
    module: dict[str, Any]


class SubmitRequest(BaseModel):
    session_id: str
    module_id: str
    answers: dict[str, Any] = Field(default_factory=dict)


class NextAction(BaseModel):
    type: Literal["module", "result"]
    module_id: str | None = None
    message: str | None = None


class SubmitResponse(BaseModel):
    session_id: str
    parameters: dict[str, Any]
    next: NextAction
    module_complete: bool


class ResultResponse(BaseModel):
    parameters: dict[str, Any]


DATA_DIR = Path(__file__).with_name("resources") / "En"
_engine_cache: tuple[tuple[tuple[str, float], ...], Engine] | None = None
_sessions: dict[str, Session] = {}


def _tokenize(expr: str) -> list[tuple[str, Any]]:
    tokens: list[tuple[str, Any]] = []
    i = 0
    length = len(expr)
    while i < length:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "()":
            tokens.append((ch, ch))
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            start = i
            while i < length and expr[i] != quote:
                i += 1
            value = expr[start:i]
            tokens.append(("STRING", value))
            i += 1
            continue
        if ch in "=!":
            if i + 1 < length and expr[i + 1] == "=":
                tokens.append(("OP", expr[i : i + 2]))
                i += 2
                continue
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch.isdigit():
            start = i
            i += 1
            while i < length and expr[i].isdigit():
                i += 1
            tokens.append(("NUMBER", int(expr[start:i])))
            continue
        if ch.isalpha() or ch in "_":
            start = i
            i += 1
            while i < length and (expr[i].isalnum() or expr[i] in "._-"):
                i += 1
            word = expr[start:i]
            lower = word.lower()
            if lower in {"and", "or", "not", "contains", "is", "defined"}:
                tokens.append(("KW", lower))
            elif lower in {"true", "false"}:
                tokens.append(("BOOL", lower == "true"))
            else:
                tokens.append(("IDENT", word))
            continue
        i += 1
    return tokens


def _parse_expression(expr: str) -> Any:
    tokens = _tokenize(expr)
    index = 0

    def peek() -> tuple[str, Any] | None:
        return tokens[index] if index < len(tokens) else None

    def consume() -> tuple[str, Any]:
        nonlocal index
        tok = tokens[index]
        index += 1
        return tok

    def parse_primary() -> Any:
        tok = peek()
        if tok is None:
            return ("lit", None)
        ttype, value = tok
        if ttype == "(":
            consume()
            node = parse_or()
            if peek() and peek()[0] == ")":
                consume()
            return node
        if ttype == "IDENT":
            consume()
            return ("var", value)
        if ttype == "STRING":
            consume()
            return ("lit", value)
        if ttype == "NUMBER":
            consume()
            return ("lit", value)
        if ttype == "BOOL":
            consume()
            return ("lit", value)
        return ("lit", None)

    def parse_comparison() -> Any:
        left = parse_primary()
        tok = peek()
        if tok and tok[0] in {"OP", "KW"}:
            if tok[0] == "OP" and tok[1] in {"==", "!="}:
                op = tok[1]
                consume()
                right = parse_primary()
                return ("cmp", op, left, right)
            if tok[0] == "KW" and tok[1] in {"contains", "is"}:
                op = tok[1]
                consume()
                if op == "is" and peek() and peek()[0] == "KW" and peek()[1] == "defined":
                    consume()
                    if left[0] == "var":
                        return ("is_defined", left[1])
                    return ("lit", False)
                right = parse_primary()
                return ("cmp", op, left, right)
        return left

    def parse_not() -> Any:
        tok = peek()
        if tok and tok[0] == "KW" and tok[1] == "not":
            consume()
            return ("not", parse_not())
        return parse_comparison()

    def parse_and() -> Any:
        node = parse_not()
        while True:
            tok = peek()
            if tok and tok[0] == "KW" and tok[1] == "and":
                consume()
                node = ("and", node, parse_not())
            else:
                break
        return node

    def parse_or() -> Any:
        node = parse_and()
        while True:
            tok = peek()
            if tok and tok[0] == "KW" and tok[1] == "or":
                consume()
                node = ("or", node, parse_and())
            else:
                break
        return node

    return parse_or()


def _eval_expr(node: Any, env: dict[str, Any]) -> Any:
    ntype = node[0]
    if ntype == "lit":
        return node[1]
    if ntype == "var":
        return env.get(node[1])
    if ntype == "not":
        return not bool(_eval_expr(node[1], env))
    if ntype == "and":
        return bool(_eval_expr(node[1], env)) and bool(_eval_expr(node[2], env))
    if ntype == "or":
        return bool(_eval_expr(node[1], env)) or bool(_eval_expr(node[2], env))
    if ntype == "is_defined":
        return node[1] in env and env.get(node[1]) is not None
    if ntype == "cmp":
        op, left_node, right_node = node[1], node[2], node[3]
        left = _eval_expr(left_node, env)
        right = _eval_expr(right_node, env)
        if left is None:
            return False
        if op in {"==", "is"}:
            return left == right
        if op == "!=":
            return left != right
        if op == "contains":
            if isinstance(left, list):
                return right in left
            if isinstance(left, str) and right is not None:
                return str(right) in left
            return False
    return False


def _parse_value(text: str) -> Any:
    if not text:
        return None
    if (text.startswith("'") and text.endswith("'")) or (text.startswith('"') and text.endswith('"')):
        return text[1:-1]
    lower = text.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def _split_inline_action(text: str) -> tuple[str, tuple[str, Any] | None]:
    if ":" in text:
        cond_part, rest = text.split(":", 1)
        action = _parse_action(rest.strip())
        return cond_part.strip(), action
    for keyword in [" SET ", " ADD "]:
        idx = text.upper().find(keyword)
        if idx != -1:
            cond = text[:idx].strip()
            action = _parse_action(text[idx + 1 :].strip())
            return cond, action
    return text.strip(), None


def _parse_action(text: str) -> tuple[str, Any] | None:
    upper = text.upper()
    if upper.startswith("SET "):
        return ("set", _parse_value(text[4:].strip()))
    if upper.startswith("ADD "):
        return ("add", _parse_value(text[4:].strip()))
    return None


def _prepare_logic_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        stripped = raw.lstrip()
        if stripped.startswith("#"):
            continue
        indent = len(raw) - len(stripped)
        lines.append((indent, stripped))
    return lines


def _parse_statements(lines: list[tuple[int, str]], start: int, base_indent: int) -> tuple[list[Any], int]:
    stmts: list[Any] = []
    i = start
    while i < len(lines):
        indent, content = lines[i]
        if indent < base_indent:
            break
        if content.startswith("ELSE"):
            break
        if content.startswith("IF "):
            stmt, i = _parse_if(lines, i, indent)
            stmts.append(stmt)
            continue
        if content.startswith("SET "):
            stmts.append(("set", _parse_value(content[4:].strip())))
            i += 1
            continue
        if content.startswith("ADD "):
            stmts.append(("add", _parse_value(content[4:].strip())))
            i += 1
            continue
        i += 1
    return stmts, i


def _parse_if(lines: list[tuple[int, str]], start: int, indent: int) -> tuple[Any, int]:
    _, content = lines[start]
    prefix = "IF "
    if content.startswith("ELSE IF "):
        prefix = "ELSE IF "
    cond_text, inline_action = _split_inline_action(content[len(prefix) :].strip())
    cond_ast = _parse_expression(cond_text)
    i = start + 1
    if inline_action:
        then_block = [inline_action]
    else:
        if i < len(lines) and lines[i][0] > indent:
            then_block, i = _parse_statements(lines, i, lines[i][0])
        else:
            then_block = []
    else_block: list[Any] | None = None
    if i < len(lines) and lines[i][0] == indent:
        next_content = lines[i][1]
        if next_content.startswith("ELSE IF "):
            else_stmt, i = _parse_if(lines, i, indent)
            else_block = [else_stmt]
        elif next_content.startswith("ELSE"):
            else_text = next_content[len("ELSE") :].strip()
            if else_text.startswith(":"):
                else_text = else_text[1:].strip()
            inline_else = _parse_action(else_text) if else_text else None
            i += 1
            if inline_else:
                else_block = [inline_else]
            else:
                if i < len(lines) and lines[i][0] > indent:
                    else_block, i = _parse_statements(lines, i, lines[i][0])
                else:
                    else_block = []
    return ("if", cond_ast, then_block, else_block), i


def _compile_logic(text: str) -> Any:
    raw = text.strip()
    if not raw:
        return ("noop",)
    lowered = raw.lower()
    if lowered.startswith("value selected in"):
        qid = raw.split("in", 1)[1].strip()
        return ("value_selected", qid)
    if lowered.startswith("true if"):
        parts = re.split(r";\s*otherwise\s+false", raw, flags=re.IGNORECASE)
        expr = parts[0][7:].strip()
        expr = _expand_or_shorthand(expr)
        return ("bool_expr", _parse_expression(expr))
    lines = _prepare_logic_lines(raw)
    if not lines:
        return ("noop",)
    stmts, _ = _parse_statements(lines, 0, lines[0][0])
    return ("block", stmts)


def _expand_or_shorthand(expr: str) -> str:
    match = re.search(r"(q[\w\.\-]+)", expr)
    if not match:
        return expr
    var = match.group(1)
    def repl(m: re.Match[str]) -> str:
        literal = m.group(1)
        return f"OR {var} is {literal}"
    return re.sub(r"\bOR\s+(['\"][^'\"]+['\"])", repl, expr)


def _execute_logic(compiled: Any, answers: dict[str, Any], params: dict[str, Any], default: Any) -> Any:
    env = {**params, **answers}
    if compiled[0] == "value_selected":
        return answers.get(compiled[1], default)
    if compiled[0] == "bool_expr":
        return bool(_eval_expr(compiled[1], env))
    if compiled[0] == "block":
        return _eval_statements(compiled[1], env, default)
    return default


def _eval_statements(stmts: list[Any], env: dict[str, Any], current: Any) -> Any:
    value = current
    for stmt in stmts:
        if stmt[0] == "set":
            value = stmt[1]
        elif stmt[0] == "add":
            if not isinstance(value, list):
                value = []
            value.append(stmt[1])
        elif stmt[0] == "if":
            cond, then_block, else_block = stmt[1], stmt[2], stmt[3]
            if _eval_expr(cond, env):
                value = _eval_statements(then_block, env, value)
            elif else_block is not None:
                value = _eval_statements(else_block, env, value)
    return value


def _parse_module_code(module_id: str, filename: str) -> str:
    match = re.match(r"^(\d+[a-z]?)_", module_id)
    if match:
        return match.group(1)
    match = re.search(r"Module(\d+[a-z]?)", filename, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return module_id


def _normalize_code(code: str) -> str:
    match = re.match(r"^0*(\d+)([a-z]?)$", code, flags=re.IGNORECASE)
    if not match:
        return code.lower()
    number, suffix = match.group(1), match.group(2).lower()
    return f"{int(number)}{suffix}"


def _code_sort_key(code: str) -> tuple[int, str]:
    match = re.match(r"^0*(\d+)([a-z]?)$", code, flags=re.IGNORECASE)
    if not match:
        return (999, code)
    return (int(match.group(1)), match.group(2) or "")


def _load_engine() -> Engine:
    if not DATA_DIR.exists():
        raise RuntimeError("resources_dir_missing")
    files = sorted(DATA_DIR.glob("*.yaml"))
    modules: list[ModuleDef] = []
    for path in files:
        raw_text = path.read_text(encoding="utf-8")
        raw_text = raw_text.replace("[cite_start]", "").replace("[cite_end]", "")
        raw = yaml.safe_load(raw_text)
        module_id = raw.get("module")
        if not module_id:
            raise RuntimeError(f"module_id_missing:{path.name}")
        module_code = _parse_module_code(module_id, path.name)
        questions_raw = raw.get("questions") or []
        questions: list[QuestionDef] = []
        for q in questions_raw:
            qid = q.get("id")
            if not qid:
                continue
            questions.append(
                QuestionDef(
                    id=qid,
                    qtype=q.get("type") or "",
                    dependency=q.get("dependency"),
                    options=q.get("options"),
                    raw=q,
                )
            )
        questions_by_id = {q.id: q for q in questions}
        updates_raw = raw.get("parameter_updates") or []
        updates: list[ParameterUpdateDef] = []
        for upd in updates_raw:
            logic = upd.get("logic") or ""
            updates.append(
                ParameterUpdateDef(
                    parameter=upd.get("parameter"),
                    param_type=upd.get("type"),
                    logic=logic,
                    compiled=_compile_logic(logic),
                )
            )
        router_raw = raw.get("router") or []
        router: list[RouterRuleDef] = []
        for rule in router_raw:
            cond = rule.get("if") or ""
            router.append(
                RouterRuleDef(
                    condition=cond,
                    compiled=_parse_expression(cond) if cond else ("lit", True),
                    action=rule.get("action") or "",
                    message=rule.get("message"),
                )
            )
        modules.append(
            ModuleDef(
                module_id=module_id,
                module_code=module_code,
                title=raw.get("title") or module_id,
                description=raw.get("description"),
                questions=questions,
                questions_by_id=questions_by_id,
                parameter_updates=updates,
                router=router,
            )
        )
    modules.sort(key=lambda m: _code_sort_key(m.module_code))
    modules_by_id = {m.module_id: m for m in modules}
    modules_by_code = {_normalize_code(m.module_code): m for m in modules}
    return Engine(modules=modules, modules_by_id=modules_by_id, modules_by_code=modules_by_code)


def _get_engine() -> Engine:
    global _engine_cache
    signature = tuple(sorted((p.name, p.stat().st_mtime) for p in DATA_DIR.glob("*.yaml")))
    if _engine_cache and _engine_cache[0] == signature:
        return _engine_cache[1]
    engine = _load_engine()
    _engine_cache = (signature, engine)
    return engine


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


def _compute_parameters(engine: Engine, answers: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for module in engine.modules:
        for update in module.parameter_updates:
            default = _default_for_type(update.param_type)
            value = _execute_logic(update.compiled, answers, params, default)
            params[update.parameter] = value
    return params


def _validate_answer(question: QuestionDef, value: Any) -> Any:
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
    if question.qtype == "multi_choice":
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


def _question_visible(question: QuestionDef, answers: dict[str, Any], params: dict[str, Any]) -> bool:
    if not question.dependency:
        return True
    env = {**params, **answers}
    return bool(_eval_expr(_parse_expression(question.dependency), env))


def _module_payload(module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    visible = [q.raw for q in module.questions if _question_visible(q, answers, params)]
    return {
        "id": module.module_id,
        "title": module.title,
        "description": module.description,
        "questions": visible,
    }


def _module_complete(module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> bool:
    for q in module.questions:
        if _question_visible(q, answers, params) and q.id not in answers:
            return False
    return True


def _next_action(engine: Engine, module: ModuleDef, answers: dict[str, Any], params: dict[str, Any]) -> NextAction:
    module_done = _module_complete(module, answers, params)
    env = {**params, **answers, "Module_finished": module_done}
    for rule in module.router:
        if rule.condition and not _eval_expr(rule.compiled, env):
            continue
        action = rule.action or ""
        action_lower = action.lower()
        if "go to module" in action_lower:
            match = re.search(r"module\s+(\d+[a-z]?)", action, flags=re.IGNORECASE)
            if not match:
                raise HTTPException(status_code=500, detail={"router_action_invalid": action})
            code = _normalize_code(match.group(1))
            target = engine.modules_by_code.get(code)
            if not target:
                raise HTTPException(status_code=500, detail={"router_target_missing": action})
            return NextAction(type="module", module_id=target.module_id, message=rule.message)
        if "end" in action_lower or "finish" in action_lower:
            return NextAction(type="result", message=rule.message)
    return NextAction(type="module", module_id=module.module_id)


def _get_session(session_id: str) -> Session:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="session_not_found")
    return session


app = FastAPI(title="AI Act Questionnaire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/init", response_model=InitResponse)
def init() -> InitResponse:
    engine = _get_engine()
    if not engine.modules:
        raise HTTPException(status_code=500, detail="no_modules_loaded")
    session_id = uuid4().hex
    session = Session(id=session_id, current_module_id=engine.modules[0].module_id)
    session.parameters = _compute_parameters(engine, session.answers)
    _sessions[session_id] = session
    module = engine.modules_by_id[session.current_module_id]
    return InitResponse(session_id=session_id, module=_module_payload(module, session.answers, session.parameters))


@app.get("/module/{module_id}", response_model=ModuleResponse)
def get_module(module_id: str, session_id: str) -> ModuleResponse:
    engine = _get_engine()
    session = _get_session(session_id)
    module = engine.modules_by_id.get(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="module_not_found")
    return ModuleResponse(module=_module_payload(module, session.answers, session.parameters))


@app.post("/submit", response_model=SubmitResponse)
def submit(req: SubmitRequest) -> SubmitResponse:
    engine = _get_engine()
    session = _get_session(req.session_id)
    module = engine.modules_by_id.get(req.module_id)
    if not module:
        raise HTTPException(status_code=404, detail="module_not_found")
    for qid, value in req.answers.items():
        question = module.questions_by_id.get(qid)
        if not question:
            raise HTTPException(status_code=400, detail={"unknown_question": qid})
        session.answers[qid] = _validate_answer(question, value)
    session.parameters = _compute_parameters(engine, session.answers)
    complete = _module_complete(module, session.answers, session.parameters)
    next_action = _next_action(engine, module, session.answers, session.parameters)
    if complete and next_action.type == "module":
        session.current_module_id = next_action.module_id
    if next_action.type == "result":
        session.current_module_id = None
    return SubmitResponse(
        session_id=session.id,
        parameters=session.parameters,
        next=next_action,
        module_complete=complete,
    )


@app.get("/result", response_model=ResultResponse)
def result(session_id: str) -> ResultResponse:
    session = _get_session(session_id)
    return ResultResponse(parameters=session.parameters)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

