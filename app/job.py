from __future__ import annotations

import json
import logging

from app.clients.storage import get_storage
from app.clients.subscriber import get_subscriber
from app.config import settings

logger = logging.getLogger(__name__)


def main() -> None:
    subscriber = get_subscriber()
    storage = get_storage()
    if not subscriber.enabled:
        raise SystemExit("PUBSUB_SUBSCRIPTION is required for job mode")

    processed = 0
    written: list[str] = []
    for _ in range(settings.job_max_batches):
        messages = subscriber.pull(settings.job_pull_max_messages)
        if not messages:
            break
        ack_ids: list[str] = []
        for received in messages:
            try:
                payload = json.loads(received.message.data.decode())
                event_type = (
                    received.message.attributes.get("event_type")
                    or payload.get("event_type")
                    or "receive"
                )
                uri = storage.write_json(event_type, payload)
                written.append(uri)
                ack_ids.append(received.ack_id)
                processed += 1
            except Exception:
                logger.exception("failed to persist pubsub message")
        subscriber.ack(ack_ids)

    print(f"processed={processed}")
    for uri in written:
        print(uri)


if __name__ == "__main__":
    main()
