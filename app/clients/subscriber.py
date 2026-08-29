from __future__ import annotations

from functools import lru_cache

from app.config import settings


class Subscriber:
    def __init__(self) -> None:
        self._subscriber = None
        self._subscription_path = ""
        if not settings.pubsub_subscription:
            return
        from google.cloud import pubsub_v1

        self._subscriber = pubsub_v1.SubscriberClient()
        subscription = settings.pubsub_subscription
        if subscription.startswith("projects/"):
            self._subscription_path = subscription
        else:
            project = settings.gcp_project
            if not project:
                raise ValueError(
                    "GCP_PROJECT is required when PUBSUB_SUBSCRIPTION is a short name"
                )
            self._subscription_path = self._subscriber.subscription_path(
                project, subscription
            )

    @property
    def enabled(self) -> bool:
        return self._subscriber is not None

    def pull(self, max_messages: int) -> list:
        if self._subscriber is None:
            raise RuntimeError("Pub/Sub subscription is not configured")
        from google.api_core.exceptions import DeadlineExceeded

        try:
            response = self._subscriber.pull(
                request={
                    "subscription": self._subscription_path,
                    "max_messages": max_messages,
                },
                timeout=30,
            )
        except DeadlineExceeded:
            return []
        return list(response.received_messages)

    def ack(self, ack_ids: list[str]) -> None:
        if self._subscriber is None or not ack_ids:
            return
        self._subscriber.acknowledge(
            request={
                "subscription": self._subscription_path,
                "ack_ids": ack_ids,
            }
        )


@lru_cache(maxsize=1)
def get_subscriber() -> Subscriber:
    return Subscriber()
