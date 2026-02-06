from __future__ import annotations

import threading
import time
from typing import Any
from uuid import uuid4
import os
import json
import logging

from fastapi import HTTPException

from ..domain.models import Session


class SessionStore:
    def __init__(self, ttl_seconds: int = 7200, cleanup_interval: int = 300) -> None:
        self._logger = logging.getLogger("aiq.session_store")
        env_ttl = os.environ.get("SESSION_TTL_SECONDS")
        env_cleanup = os.environ.get("SESSION_CLEANUP_INTERVAL")
        self._ttl_seconds = int(env_ttl) if env_ttl and env_ttl.isdigit() else ttl_seconds
        self._cleanup_interval = int(env_cleanup) if env_cleanup and env_cleanup.isdigit() else cleanup_interval
        self._lock = threading.Lock()
        self._sessions: dict[str, Session] = {}
        self._last_access: dict[str, float] = {}
        self._redis = None
        url = os.environ.get("REDIS_URL") or os.environ.get("SESSION_REDIS_URL")
        if url:
            try:
                import redis
                self._redis = redis.Redis.from_url(url, decode_responses=True)
                self._logger.info("redis_enabled=true url=%s", url)
            except Exception:
                self._redis = None
                self._logger.exception("redis_connect_failed url=%s", url)
        if not self._redis:
            self._logger.info("redis_enabled=false")
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
        if self._redis:
            self._redis.setex(self._key(session_id), self._ttl_seconds, self._dump(session))
        else:
            with self._lock:
                self._sessions[session_id] = session
                self._last_access[session_id] = time.time()
        self._logger.info("session_create id=%s module=%s lang=%s", session_id, first_module_id, lang)
        return session

    def get(self, session_id: str) -> Session:
        if self._redis:
            raw = self._redis.get(self._key(session_id))
            if not raw:
                self._logger.warning("session_not_found id=%s backend=redis", session_id)
                raise HTTPException(status_code=404, detail="session_not_found")
            session = self._load(raw)
            self._redis.expire(self._key(session_id), self._ttl_seconds)
            return session
        else:
            with self._lock:
                session = self._sessions.get(session_id)
                if not session:
                    self._logger.warning("session_not_found id=%s backend=memory", session_id)
                    raise HTTPException(status_code=404, detail="session_not_found")
                self._last_access[session_id] = time.time()
                return session

    def update_parameters(self, session: Session, params: dict[str, Any]) -> None:
        with self._lock:
            session.parameters = params

    def save(self, session: Session) -> None:
        if self._redis:
            self._redis.setex(self._key(session.id), self._ttl_seconds, self._dump(session))
        else:
            with self._lock:
                self._sessions[session.id] = session
                self._last_access[session.id] = time.time()
        self._logger.info(
            "session_save id=%s module=%s answers=%d params=%d",
            session.id,
            session.current_module_id,
            len(session.answers),
            len(session.parameters),
        )

    def _key(self, session_id: str) -> str:
        return f"aiq:sessions:{session_id}"

    def _dump(self, session: Session) -> str:
        return json.dumps(
            {
                "id": session.id,
                "answers": session.answers,
                "parameters": session.parameters,
                "current_module_id": session.current_module_id,
                "lang": session.lang,
                "conclusion": session.conclusion,
            }
        )

    def _load(self, raw: str) -> Session:
        data = json.loads(raw)
        return Session(
            id=data.get("id"),
            answers=data.get("answers") or {},
            parameters=data.get("parameters") or {},
            current_module_id=data.get("current_module_id"),
            lang=data.get("lang") or "en",
            conclusion=data.get("conclusion"),
        )
