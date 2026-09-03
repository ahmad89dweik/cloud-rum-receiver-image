"""HTTP surface for the exposures stream. No logic lives here."""

from fastapi import APIRouter, Header, Response, status

from app.pipelines.exposures import service
from app.pipelines.exposures.schemas import ExposureEvent

router = APIRouter(tags=["exposures"])


@router.post("/exposures", status_code=status.HTTP_204_NO_CONTENT)
async def receive_exposure(
    event: ExposureEvent,
    user_agent: str | None = Header(default=None),
) -> Response:
    await service.handle(event, user_agent)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
