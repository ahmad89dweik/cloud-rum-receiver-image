"""Application factory — wires routers and middleware. No business logic."""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.routers import router as core_router
from app.core.settings import get_settings
from app.observability.middleware import RequestLogMiddleware
from app.messaging.publisher import pub

@asynccontextmanager
async def lifespan(app: FastAPI):
    pub.start()
    yield
    pub.stop()

def create_app() -> FastAPI:
    settings = get_settings()

    
            
    app = FastAPI(
        title=settings.service_name,
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )

    app.add_middleware(RequestLogMiddleware)

    app.include_router(core_router)

    return app


app = create_app()
