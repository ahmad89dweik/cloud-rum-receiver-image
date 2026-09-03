"""Builds the Pub/Sub wire format: message body and attributes."""

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    body: bytes
    attributes: dict[str, str]


def build(
    record: dict,
    *,
    event_type: str,
    schema_version: int,
) -> Message:
    payload = {**record, "schema_version": schema_version}

    body = json.dumps(
        payload,
        separators=(",", ":"),
        ensure_ascii=False,  
    ).encode("utf-8")

    return Message(
        body=body,
        attributes={"event_type": event_type},
    )