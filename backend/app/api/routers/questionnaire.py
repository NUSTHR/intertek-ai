from fastapi import APIRouter, Depends

from ..schemas import ModuleResponse, QuestionResponse, ResultResponse, StartResponse, SubmitAnswerRequest, SubmitResponse
from ...container import get_service
from ...services.questionnaire import QuestionnaireService

router = APIRouter()


@router.post("/start", response_model=StartResponse)
def start(lang: str = "en", service: QuestionnaireService = Depends(get_service)) -> StartResponse:
    session_id, module = service.start(lang)
    return StartResponse(session_id=session_id, module=module)


@router.get("/module/{module_id}", response_model=ModuleResponse)
def get_module(
    module_id: str, session_id: str, lang: str | None = None, service: QuestionnaireService = Depends(get_service)
) -> ModuleResponse:
    module = service.get_module(session_id, module_id, lang)
    return ModuleResponse(module=module)


@router.post("/submit-answer", response_model=SubmitResponse)
def submit_answer(
    req: SubmitAnswerRequest, lang: str | None = None, service: QuestionnaireService = Depends(get_service)
) -> SubmitResponse:
    payload = service.submit_answer(req.session_id, req.module_id, req.answers, req.replace, lang)
    return SubmitResponse(
        session_id=payload["session_id"],
        parameters=payload["parameters"],
        next=payload["next"],
        module_complete=payload["module_complete"],
        module=payload["module"],
        conclusion=payload["conclusion"],
    )


@router.get("/result", response_model=ResultResponse)
def result(
    session_id: str, lang: str | None = None, service: QuestionnaireService = Depends(get_service)
) -> ResultResponse:
    parameters, conclusion = service.result(session_id, lang)
    return ResultResponse(parameters=parameters, conclusion=conclusion)


@router.get("/question/{question_id}", response_model=QuestionResponse)
def get_question(question_id: str, lang: str | None = None, service: QuestionnaireService = Depends(get_service)) -> QuestionResponse:
    question = service.get_question(question_id, lang)
    return QuestionResponse(question=question)
