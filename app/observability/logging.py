"""Structured JSON logging in the field names Cloud Logging understands.

``severity`` (not ``level``) is what Cloud Logging reads to colour and filter
entries. Getting that name wrong makes every line render as INFO, including
errors, which silently breaks alerting.
"""

import json
import logging
import sys
from typing import Any

from app.observability.trace import formatted_trace

_RESERVED = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
) | {
    "message",
    "asctime",
    "taskName",
    "color_message",
}


class CloudLoggingFormatter(logging.Formatter):
    def __init__(self, project: str = "") -> None:
        super().__init__()
        self._project = project

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        trace = formatted_trace(self._project)
        if trace:
            payload["logging.googleapis.com/trace"] = trace

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key not in _RESERVED and not key.startswith("_"):
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging(project: str = "", level: str = "INFO") -> None:
    """Install the JSON formatter as the only stdout handler.

    Must run before uvicorn starts, otherwise uvicorn's own handlers win and
    the output arrives unstructured.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CloudLoggingFormatter(project))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())

    # uvicorn installs its own handlers; make them propagate to ours instead.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
