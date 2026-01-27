from __future__ import annotations

import threading
import time
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from ..domain.models import Session


class SessionStore:
    def __init__(self, ttl_seconds: int = 7200, cleanup_interval: int = 300) -> None:
        self._sessions: dict[str, Session] = {}
        self._last_access: dict[str, float] = {}
        self._ttl_seconds = ttl_seconds
        self._cleanup_interval = cleanup_interval
        self._lock = threading.Lock()
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_loop(self) -> None:
        while True:
            time.sleep(self._cleanup_interval)
            now = time.time()
            with self._lock:
                expired = [sid for sid, ts in self._last_access.items() if now - ts > self._ttl_seconds]
                for sid in expired:
                    self._sessions.pop(sid, None)
                    self._last_access.pop(sid, None)

    def create(self, first_module_id: str, lang: str) -> Session:
        session_id = uuid4().hex
        session = Session(id=session_id, current_module_id=first_module_id, lang=lang)
        with self._lock:
            self._sessions[session_id] = session
            self._last_access[session_id] = time.time()
        return session

    def get(self, session_id: str) -> Session:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="session_not_found")
            self._last_access[session_id] = time.time()
            return session

    def update_parameters(self, session: Session, params: dict[str, Any]) -> None:
        with self._lock:
            session.parameters = params
