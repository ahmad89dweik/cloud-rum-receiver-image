"""Exposure handling.

Current scope: enrich and log. Publishing to Pub/Sub is not wired yet — that
lands in ``app.messaging`` and gets called from here.
"""

import logging
import uuid
from datetime import UTC, datetime

from app.messaging.publisher import pub
from app.messaging.envelope import build
from app.observability.trace import current_trace
from app.pipelines.exposures.schemas import ExposureEvent, SCHEMA_VERSION

logger = logging.getLogger("exposures")

EVENT_TYPE = "exposure"

def enrich(event: ExposureEvent, user_agent: str | None) -> dict:
    """Add server-derived fields. Never trust client values we can derive."""
    payload = event.model_dump(mode="json", exclude_none=True)
    return {
        "event_id": payload.pop("event_id",None) or str(uuid.uuid4()),
        "server_ts": datetime.now(UTC).isoformat(),
        "trace_id": current_trace(),
        "user_agent": user_agent,
        "payload": payload,
    }


async def handle(event: ExposureEvent, user_agent: str | None) -> None:
    record = enrich(event, user_agent)
    message = build(
        record,
        event_type=EVENT_TYPE,
        schema_version=SCHEMA_VERSION,
    )
    try:
        message_id = await pub.publish(message.body, message.attributes)
    except Exception as e:
        logger.exception("publish failed, event dropped",extra={"event_id": record["event_id"],"event": record})
        return
    logger.debug("exposure published", extra={"event_id": record["event_id"]})