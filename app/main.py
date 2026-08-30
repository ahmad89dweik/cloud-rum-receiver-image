"""Application factory — wires routers and middleware. No business logic."""

from fastapi import FastAPI

from app import health
from app.observability.middleware import RequestLogMiddleware
from app.pipelines.exposures.router import router as exposures_router
from app.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.service_name,
        docs_url=None,
        redoc_url=None,
    )

    app.add_middleware(RequestLogMiddleware)

    app.include_router(health.router)
    app.include_router(exposures_router, prefix="/v1")

    return app


app = create_app()
