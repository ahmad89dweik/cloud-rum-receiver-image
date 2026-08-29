from fastapi import FastAPI

from app.routers.receive import router


def create_app() -> FastAPI:
    application = FastAPI(title="cloud-rum-receiver-poc")
    application.include_router(router)

    @application.get("/")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
