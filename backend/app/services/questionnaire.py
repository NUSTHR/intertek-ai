from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from ..domain.models import Engine, Session
from ..infra.loader import EngineLoader
from ..infra.store import SessionStore
from ..logic.evaluator import Evaluator


class QuestionnaireService:
    def __init__(self, loaders: dict[str, EngineLoader], evaluator: Evaluator, store: SessionStore) -> None:
        self.loaders = loaders
        self.evaluator = evaluator
        self.store = store

    def start(self, lang: str | None = None) -> tuple[str, dict[str, Any]]:
        lang_value = self._normalize_lang(lang)
        engine = self._engine(lang_value)
        if not engine.modules:
            raise HTTPException(status_code=500, detail="no_modules_loaded")
        session = self.store.create(engine.modules[0].module_id, lang_value)
        session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        module = engine.modules_by_id[session.current_module_id]
        self.store.save(session)
        return session.id, self.evaluator.module_payload(module, session.answers, session.parameters)

    def get_module(self, session_id: str, module_id: str, lang: str | None = None) -> dict[str, Any]:
        session = self.store.get(session_id)
        lang_value = self._normalize_lang(lang, session)
        engine = self._engine(lang_value)
        session.lang = lang_value
        module = engine.modules_by_id.get(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="module_not_found")
        self.store.save(session)
        return self.evaluator.module_payload(module, session.answers, session.parameters)

    def submit_answer(
        self,
        session_id: str,
        module_id: str | None,
        answers: dict[str, Any],
        replace: bool = False,
        lang: str | None = None,
    ) -> dict[str, Any]:
        session = self.store.get(session_id)
        lang_value = self._normalize_lang(lang, session)
        engine = self._engine(lang_value)
        session.lang = lang_value
        active_module_id = module_id or session.current_module_id
        if not active_module_id:
            raise HTTPException(status_code=400, detail="module_id_required")
        module = engine.modules_by_id.get(active_module_id)
        if not module:
            raise HTTPException(status_code=404, detail="module_not_found")
        if module_id:
            session.current_module_id = active_module_id
        if replace:
            session.answers = {}
        all_questions: dict[str, Any] = {}
        for mod in engine.modules:
            for q in mod.questions:
                all_questions[q.id] = q
        for qid, value in answers.items():
            question = all_questions.get(qid)
            if not question:
                raise HTTPException(status_code=400, detail={"unknown_question": qid})
            session.answers[qid] = self.evaluator.validate_answer(question, value)
        session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        for _ in range(5):
            if not self.evaluator.prune_hidden_answers(module, session.answers, session.parameters):
                break
            session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        complete = self.evaluator.module_complete(module, session.answers, session.parameters)
        if not complete:
            next_type, next_module_id, message = ("module", module.module_id, None)
        else:
            next_type, next_module_id, message = self.evaluator.next_action(
                module, session.answers, session.parameters
            )
        next_module_payload = None
        conclusion = None
        if not complete:
            next_module_payload = self.evaluator.module_payload(module, session.answers, session.parameters)
        elif next_type == "module":
            session.current_module_id = next_module_id
            next_module = engine.modules_by_id.get(next_module_id) if next_module_id else None
            if next_module:
                next_module_payload = self.evaluator.module_payload(next_module, session.answers, session.parameters)
        if next_type == "result":
            session.current_module_id = None
            conclusion = self.evaluator.compute_conclusion(session.parameters)
            session.conclusion = conclusion
        self.store.save(session)
        return {
            "session_id": session.id,
            "parameters": session.parameters,
            "next": {"type": next_type, "module_id": next_module_id, "message": message},
            "module_complete": complete,
            "module": next_module_payload,
            "conclusion": conclusion,
        }

    def result(self, session_id: str, lang: str | None = None) -> tuple[dict[str, Any], dict[str, Any] | None]:
        session = self.store.get(session_id)
        lang_value = self._normalize_lang(lang, session)
        engine = self._engine(lang_value)
        session.lang = lang_value
        session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        conclusion = self.evaluator.compute_conclusion(session.parameters)
        session.conclusion = conclusion
        self.store.save(session)
        return session.parameters, conclusion

    def get_question(self, question_id: str, lang: str | None = None) -> dict[str, Any]:
        lang_value = self._normalize_lang(lang)
        engine = self._engine(lang_value)
        for module in engine.modules:
            question = module.questions_by_id.get(question_id)
            if question:
                return question.raw
        raise HTTPException(status_code=404, detail="question_not_found")

    def _engine(self, lang: str) -> Engine:
        loader = self.loaders.get(lang) or self.loaders.get("en")
        if not loader:
            raise HTTPException(status_code=500, detail="engine_loader_missing")
        return loader.get_engine()

    def _normalize_lang(self, lang: str | None, session: Session | None = None) -> str:
        raw = (lang or (session.lang if session else "") or "en").lower()
        if raw in {"zh", "cn", "zh-cn", "zh-hans", "zh-hans-cn"}:
            return "cn"
        return "en"
