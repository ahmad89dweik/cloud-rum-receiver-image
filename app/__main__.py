"""Process entry point.

Reads ``$PORT`` in Python rather than a shell so that Python stays PID 1 and
Cloud Run's SIGTERM reaches uvicorn, letting in-flight work drain on scale-down.
Logging is configured before uvicorn starts, or uvicorn's own handlers win.
"""

import uvicorn

from app.observability.logging import configure_logging
from app.settings import get_settings


def run() -> None:
    settings = get_settings()
    configure_logging(project=settings.gcp_project, level=settings.log_level)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=None,
        access_log=False,
    )


if __name__ == "__main__":
    run()
