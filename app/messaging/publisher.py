"""Pub/Sub publisher: batch settings and lifespan flush. Not wired yet."""
import logging

from google.cloud import pubsub_v1
from starlette.concurrency import run_in_threadpool

from app.core.settings import get_settings

logger = logging.getLogger("publisher")

class Publisher:
    def __init__(self):
        self._client : pubsub_v1.PublisherClient | None = None
        self._topic_path : str = ""
    
    def start(self) -> None:
        settings = get_settings()
        self._client = pubsub_v1.PublisherClient(
            batch_settings=pubsub_v1.types.BatchSettings(
                max_messages = settings.publish_max_messages,
                max_bytes = settings.publish_max_bytes,
                max_latency = settings.publish_max_latency,
            ),
        )
        self._topic_path = settings.topic_path
    async def publish(self, body: bytes, attributes: dict[str, str]) -> str:
        if self._client is None:
            raise RuntimeError("Publisher not started")
        future = self._client.publish(self._topic_path,data=body, **attributes)
        return await run_in_threadpool(future.result,get_settings().publish_time_seconds)

    def stop(self) -> None:
        if self._client:
            self._client.stop()
            self._client = None
            self._topic_path = ""
            logger.info("Publisher stopped")

pub = Publisher()