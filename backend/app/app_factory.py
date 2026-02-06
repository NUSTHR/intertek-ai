from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from logging.handlers import RotatingFileHandler
import os
import time
import uuid

from .api.routers import router as api_router


def _setup_logging() -> logging.Logger:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_file = os.environ.get("LOG_FILE", "logs/app.log").strip()
    max_bytes = int(os.environ.get("LOG_MAX_BYTES", "10485760"))
    backup_count = int(os.environ.get("LOG_BACKUP_COUNT", "5"))
    log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        for logger_name in ("aiq", "uvicorn.error", "uvicorn.access", "uvicorn.asgi"):
            target = logging.getLogger(logger_name)
            if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", None) == file_handler.baseFilename for h in target.handlers):
                target.addHandler(file_handler)
    return logging.getLogger("aiq")


def create_app() -> FastAPI:
    logger = _setup_logging()
    app = FastAPI(title="AI Act Questionnaire API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging(request: Request, call_next):
        request_id = uuid.uuid4().hex
        start = time.perf_counter()
        if logger.isEnabledFor(logging.INFO):
            logger.info(
                "request_start id=%s method=%s path=%s query=%s client=%s ua=%s",
                request_id,
                request.method,
                request.url.path,
                request.url.query,
                request.client.host if request.client else "",
                request.headers.get("user-agent", ""),
            )
        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start) * 1000
            if logger.isEnabledFor(logging.INFO):
                logger.info(
                    "request_end id=%s status=%s duration_ms=%.2f",
                    request_id,
                    response.status_code,
                    duration_ms,
                )
            return response
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception("request_error id=%s duration_ms=%.2f", request_id, duration_ms)
            raise

    app.include_router(api_router)
    return app
