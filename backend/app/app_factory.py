from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import time
import uuid

from .api.routers import router as api_router


def create_app() -> FastAPI:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("aiq")
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
