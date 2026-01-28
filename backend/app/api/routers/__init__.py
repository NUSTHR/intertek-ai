from fastapi import APIRouter

from .health import router as health_router
from .questionnaire import router as questionnaire_router

router = APIRouter()
router.include_router(questionnaire_router)
router.include_router(health_router)
