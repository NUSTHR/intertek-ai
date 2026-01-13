from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any, Literal, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import yaml

AnswerValue = Literal["yes", "no"]


class NextQuestion(BaseModel):
    type: Literal["question"]
    id: str


class NextResult(BaseModel):
    type: Literal["result"]
    id: Literal["A", "B", "C", "D", "E"]


NextNode = Annotated[Union[NextQuestion, NextResult], Field(discriminator="type")]


class Option(BaseModel):
    label: str
    value: AnswerValue
    next: NextNode


class Question(BaseModel):
    id: str
    title: str
    description: str | None = None
    bullets: list[str] | None = None
    options: list[Option]


class Result(BaseModel):
    id: Literal["A", "B", "C", "D", "E"]
    title: str
    description: str
    bullets: list[str] | None = None


class QuestionnaireFile(BaseModel):
    start: str
    questions: list[Question]
    results: list[Result]


@dataclass(frozen=True)
class QuestionnaireIndex:
    start: str
    questions: list[Question]
    results: list[Result]
    questions_by_id: dict[str, Question]
    results_by_id: dict[str, Result]


DATA_FILE = Path(__file__).with_name("questionnaire.yaml")
_cache: tuple[float, QuestionnaireIndex] | None = None


def _load_from_yaml() -> QuestionnaireIndex:
    if not DATA_FILE.exists():
        raise RuntimeError("questionnaire_yaml_missing")

    raw = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    file_data = QuestionnaireFile.model_validate(raw)

    questions_by_id: dict[str, Question] = {}
    for q in file_data.questions:
        if q.id in questions_by_id:
            raise RuntimeError(f"duplicate_question_id:{q.id}")
        questions_by_id[q.id] = q

    results_by_id: dict[str, Result] = {}
    for r in file_data.results:
        if r.id in results_by_id:
            raise RuntimeError(f"duplicate_result_id:{r.id}")
        results_by_id[r.id] = r

    if file_data.start not in questions_by_id:
        raise RuntimeError("start_question_not_found")

    return QuestionnaireIndex(
        start=file_data.start,
        questions=file_data.questions,
        results=file_data.results,
        questions_by_id=questions_by_id,
        results_by_id=results_by_id,
    )


def get_index() -> QuestionnaireIndex:
    global _cache
    try:
        mtime = DATA_FILE.stat().st_mtime
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="questionnaire_yaml_missing")

    if _cache is not None and _cache[0] == mtime:
        return _cache[1]

    try:
        idx = _load_from_yaml()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    _cache = (mtime, idx)
    return idx


class EvaluateRequest(BaseModel):
    answers: dict[str, AnswerValue] = Field(default_factory=dict)


class EvaluateResponse(BaseModel):
    result_id: Literal["A", "B", "C", "D", "E"]
    path: list[str]
    result: Result


app = FastAPI(title="AI Questionnaire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tree")
def get_tree() -> dict[str, Any]:
    idx = get_index()
    return {"start": idx.start, "questions": idx.questions}


@app.get("/api/results")
def get_results() -> dict[str, Any]:
    idx = get_index()
    return {"results": idx.results}


def _evaluate(answers: dict[str, AnswerValue]) -> tuple[str, list[str]]:
    idx = get_index()
    current_id = idx.start
    path: list[str] = []
    while True:
        question = idx.questions_by_id.get(current_id)
        if question is None:
            raise HTTPException(status_code=500, detail="question_not_found")

        path.append(current_id)
        answer = answers.get(current_id)
        if answer is None:
            raise HTTPException(status_code=400, detail={"missing_answer": current_id, "path": path})

        selected = next((opt for opt in question.options if opt.value == answer), None)
        if selected is None:
            raise HTTPException(status_code=400, detail={"invalid_answer": current_id, "value": answer})

        nxt = selected.next
        if nxt.type == "result":
            return nxt.id, path

        current_id = nxt.id


@app.post("/api/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> EvaluateResponse:
    result_id, path = _evaluate(req.answers)
    idx = get_index()
    result = idx.results_by_id.get(result_id)
    if result is None:
        raise HTTPException(status_code=500, detail="result_not_found")
    return EvaluateResponse(result_id=result_id, path=path, result=result)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

