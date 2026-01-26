from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from ..domain.models import Engine
from ..infra.loader import EngineLoader
from ..infra.store import SessionStore
from ..logic.evaluator import Evaluator


class QuestionnaireService:
    def __init__(self, loader: EngineLoader, evaluator: Evaluator, store: SessionStore) -> None:
        self.loader = loader
        self.evaluator = evaluator
        self.store = store

    def start(self) -> tuple[str, dict[str, Any]]:
        engine = self._engine()
        if not engine.modules:
            raise HTTPException(status_code=500, detail="no_modules_loaded")
        session = self.store.create(engine.modules[0].module_id)
        session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        module = engine.modules_by_id[session.current_module_id]
        return session.id, self.evaluator.module_payload(module, session.answers, session.parameters)

    def get_module(self, session_id: str, module_id: str) -> dict[str, Any]:
        engine = self._engine()
        session = self.store.get(session_id)
        module = engine.modules_by_id.get(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="module_not_found")
        return self.evaluator.module_payload(module, session.answers, session.parameters)

    def submit_answer(
        self,
        session_id: str,
        module_id: str | None,
        answers: dict[str, Any],
        replace: bool = False,
    ) -> dict[str, Any]:
        engine = self._engine()
        session = self.store.get(session_id)
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
        return {
            "session_id": session.id,
            "parameters": session.parameters,
            "next": {"type": next_type, "module_id": next_module_id, "message": message},
            "module_complete": complete,
            "module": next_module_payload,
            "conclusion": conclusion,
        }

    def result(self, session_id: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
        engine = self._engine()
        session = self.store.get(session_id)
        session.parameters = self.evaluator.compute_parameters(engine, session.answers)
        conclusion = self.evaluator.compute_conclusion(session.parameters)
        session.conclusion = conclusion
        return session.parameters, conclusion

    def _engine(self) -> Engine:
        return self.loader.get_engine()
