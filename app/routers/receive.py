from typing import Any

from fastapi import APIRouter, Request

from app.clients.publisher import get_publisher
from app.clients.storage import get_storage
from app.schemas import ExposurePayload

router = APIRouter()


async def _body(request: Request) -> dict[str, Any]:
    try:
        payload = await request.json()
    except Exception:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"data": payload}


def _ingest(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = ExposurePayload.model_validate(payload).model_dump(exclude_none=True)
    body.setdefault("event_type", event_type)
    publisher = get_publisher()
    if publisher.enabled:
        message_id = publisher.publish(event_type, body)
        return {"ok": True, "event_type": event_type, "message_id": message_id}
    uri = get_storage().write_json(event_type, body)
    return {"ok": True, "event_type": event_type, "uri": uri}


@router.post("/receive")
async def receive(request: Request) -> dict[str, Any]:
    return _ingest("receive", await _body(request))


@router.post("/showTemplate")
async def show_template(request: Request) -> dict[str, Any]:
    return _ingest("showTemplate", await _body(request))


@router.post("/showOffer")
async def show_offer(request: Request) -> dict[str, Any]:
    return _ingest("showOffer", await _body(request))
