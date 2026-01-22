from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QuestionDef:
    id: str
    qtype: str
    dependency: str | None
    options: list[dict[str, Any]] | None
    raw: dict[str, Any]


@dataclass
class VariableRuleDef:
    condition: str
    value: Any


@dataclass
class VariableDef:
    name: str
    var_type: str | None
    rules: list[VariableRuleDef]


@dataclass
class RouterRuleDef:
    condition: str
    action: str
    target_module_id: str | None
    message: str | None


@dataclass
class ModuleDef:
    module_id: str
    module_num: int
    title: str
    description: str | None
    questions: list[QuestionDef]
    questions_by_id: dict[str, QuestionDef]
    variables: list[VariableDef]
    router: list[RouterRuleDef]


@dataclass
class Engine:
    modules: list[ModuleDef]
    modules_by_id: dict[str, ModuleDef]


@dataclass
class Session:
    id: str
    answers: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    current_module_id: str | None = None
    conclusion: dict[str, Any] | None = None
