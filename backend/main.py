from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app.api.schemas import ModuleResponse, QuestionResponse, ResultResponse, StartResponse, SubmitAnswerRequest, SubmitResponse
from .app.infra.loader import EngineLoader
from .app.infra.store import SessionStore
from .app.logic.evaluator import Evaluator
from .app.services.questionnaire import QuestionnaireService

DATA_DIR_EN = Path(__file__).parent / "app" / "resources" / "En"
DATA_DIR_CN = Path(__file__).parent / "app" / "resources" / "Cn"
loaders = {
    "en": EngineLoader(DATA_DIR_EN),
    "cn": EngineLoader(DATA_DIR_CN),
}
evaluator = Evaluator()
store = SessionStore()
service = QuestionnaireService(loaders, evaluator, store)

app = FastAPI(title="AI Act Questionnaire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/start", response_model=StartResponse)
def start(lang: str = "en") -> StartResponse:
    session_id, module = service.start(lang)
    return StartResponse(session_id=session_id, module=module)


@app.get("/module/{module_id}", response_model=ModuleResponse)
def get_module(module_id: str, session_id: str, lang: str | None = None) -> ModuleResponse:
    module = service.get_module(session_id, module_id, lang)
    return ModuleResponse(module=module)


@app.post("/submit-answer", response_model=SubmitResponse)
def submit_answer(req: SubmitAnswerRequest, lang: str | None = None) -> SubmitResponse:
    payload = service.submit_answer(req.session_id, req.module_id, req.answers, req.replace, lang)
    return SubmitResponse(
        session_id=payload["session_id"],
        parameters=payload["parameters"],
        next=payload["next"],
        module_complete=payload["module_complete"],
        module=payload["module"],
        conclusion=payload["conclusion"],
    )


@app.get("/result", response_model=ResultResponse)
def result(session_id: str, lang: str | None = None) -> ResultResponse:
    parameters, conclusion = service.result(session_id, lang)
    return ResultResponse(parameters=parameters, conclusion=conclusion)


@app.get("/question/{question_id}", response_model=QuestionResponse)
def get_question(question_id: str, lang: str | None = None) -> QuestionResponse:
    question = service.get_question(question_id, lang)
    return QuestionResponse(question=question)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
