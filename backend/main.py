from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app.api.schemas import ModuleResponse, ResultResponse, StartResponse, SubmitAnswerRequest, SubmitResponse
from .app.infra.loader import EngineLoader
from .app.infra.store import SessionStore
from .app.logic.evaluator import Evaluator
from .app.services.questionnaire import QuestionnaireService

DATA_DIR = Path(__file__).parent / "app" / "resources" / "En"
loader = EngineLoader(DATA_DIR)
evaluator = Evaluator()
store = SessionStore()
service = QuestionnaireService(loader, evaluator, store)

app = FastAPI(title="AI Act Questionnaire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/start", response_model=StartResponse)
def start() -> StartResponse:
    session_id, module = service.start()
    return StartResponse(session_id=session_id, module=module)


@app.get("/module/{module_id}", response_model=ModuleResponse)
def get_module(module_id: str, session_id: str) -> ModuleResponse:
    module = service.get_module(session_id, module_id)
    return ModuleResponse(module=module)


@app.post("/submit-answer", response_model=SubmitResponse)
def submit_answer(req: SubmitAnswerRequest) -> SubmitResponse:
    payload = service.submit_answer(req.session_id, req.module_id, req.answers)
    return SubmitResponse(
        session_id=payload["session_id"],
        parameters=payload["parameters"],
        next=payload["next"],
        module_complete=payload["module_complete"],
        module=payload["module"],
        conclusion=payload["conclusion"],
    )


@app.get("/result", response_model=ResultResponse)
def result(session_id: str) -> ResultResponse:
    parameters, conclusion = service.result(session_id)
    return ResultResponse(parameters=parameters, conclusion=conclusion)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
