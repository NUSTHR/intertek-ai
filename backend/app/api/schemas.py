from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class StartResponse(BaseModel):
    session_id: str
    module: dict[str, Any]


class ModuleResponse(BaseModel):
    module: dict[str, Any]


class SubmitAnswerRequest(BaseModel):
    session_id: str
    module_id: str | None = None
    answers: dict[str, Any] = Field(default_factory=dict)
    replace: bool = False


class NextAction(BaseModel):
    type: Literal["module", "result"]
    module_id: str | None = None
    message: str | None = None


class SubmitResponse(BaseModel):
    session_id: str
    parameters: dict[str, Any]
    next: NextAction
    module_complete: bool
    module: dict[str, Any] | None = None
    conclusion: dict[str, Any] | None = None


class ResultResponse(BaseModel):
    parameters: dict[str, Any]
    conclusion: dict[str, Any] | None = None
