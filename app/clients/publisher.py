from __future__ import annotations

import json
from functools import lru_cache

from app.config import settings


class Publisher:
    def __init__(self) -> None:
        self._publisher = None
        self._topic_path = ""
        if not settings.pubsub_topic:
            return
        from google.cloud import pubsub_v1

        self._publisher = pubsub_v1.PublisherClient()
        topic = settings.pubsub_topic
        if topic.startswith("projects/"):
            self._topic_path = topic
        else:
            project = settings.gcp_project
            if not project:
                raise ValueError("GCP_PROJECT is required when PUBSUB_TOPIC is a short name")
            self._topic_path = self._publisher.topic_path(project, topic)

    @property
    def enabled(self) -> bool:
        return self._publisher is not None

    def publish(self, event_type: str, payload: dict) -> str:
        if self._publisher is None:
            raise RuntimeError("Pub/Sub is not configured")
        data = json.dumps(payload, separators=(",", ":")).encode()
        future = self._publisher.publish(
            self._topic_path,
            data,
            event_type=event_type,
        )
        return future.result(timeout=10)


@lru_cache(maxsize=1)
def get_publisher() -> Publisher:
    return Publisher()
