import uvicorn

from app.config import settings
from app.main import app


def main() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level,
    )


if __name__ == "__main__":
    main()
