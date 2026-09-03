"""Exposure payload model.

Deliberately permissive: ``extra="allow"`` keeps fields the FRE starts sending
before we deploy a schema change. Strict validation here would silently drop
exactly the data this pipeline exists to capture.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

SCHEMA_VERSION = 1

class ExposureEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    uid: str | None = None
    template: str | None = None
    offer: str | None = None
    term: str | None = None
    url: str | None = None
    event_type: str | None = None
    client_ts: datetime | None = None
