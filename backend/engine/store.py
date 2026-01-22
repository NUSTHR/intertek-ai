from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from .models import Session


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self, first_module_id: str) -> Session:
        session_id = uuid4().hex
        session = Session(id=session_id, current_module_id=first_module_id)
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session:
        session = self._sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="session_not_found")
        return session

    def update_parameters(self, session: Session, params: dict[str, Any]) -> None:
        session.parameters = params
