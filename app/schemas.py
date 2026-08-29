from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExposurePayload(BaseModel):
    """Loose event body so burst tests can send almost anything."""

    model_config = ConfigDict(extra="allow")

    event_id: str | None = None
    event_type: str | None = None
    payload: dict[str, Any] | None = None


class PubSubEnvelope(BaseModel):
    """Placeholder for a later Pub/Sub push/pull wrapper."""

    model_config = ConfigDict(extra="allow")

    message_id: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
    data: ExposurePayload | dict[str, Any] | None = None
