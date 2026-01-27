from .config import DATA_DIR_CN, DATA_DIR_EN
from .infra.loader import EngineLoader
from .infra.store import SessionStore
from .logic.evaluator import Evaluator
from .services.questionnaire import QuestionnaireService

loaders = {
    "en": EngineLoader(DATA_DIR_EN),
    "cn": EngineLoader(DATA_DIR_CN),
}
evaluator = Evaluator()
store = SessionStore()
service = QuestionnaireService(loaders, evaluator, store)


def get_service() -> QuestionnaireService:
    return service
