"""Exposure handling.

Current scope: enrich and log. Publishing to Pub/Sub is not wired yet — that
lands in ``app.messaging`` and gets called from here.
"""

import logging
import uuid
from datetime import UTC, datetime

from app.observability.trace import current_trace
from app.pipelines.exposures.schemas import ExposureEvent

logger = logging.getLogger("exposures")


def enrich(event: ExposureEvent, user_agent: str | None) -> dict:
    """Add server-derived fields. Never trust client values we can derive."""
    return {
        "event_id": str(uuid.uuid4()),
        "server_ts": datetime.now(UTC).isoformat(),
        "trace_id": current_trace(),
        "user_agent": user_agent,
        "payload": event.model_dump(mode="json", exclude_none=True),
    }


async def handle(event: ExposureEvent, user_agent: str | None) -> None:
    record = enrich(event, user_agent)
    logger.info("exposure received", extra={"exposure": record})
