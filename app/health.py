"""Liveness and readiness.

Separate endpoints because the answers differ. A service that cannot reach its
downstream is *unready* (stop routing to it) but not *dead* (restarting will
not fix the downstream).
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def healthz() -> dict[str, str]:
    """Liveness — the process is up. Never touches dependencies."""
    return {"status": "ok"}


@router.get("/ready")
async def readyz() -> dict[str, str]:
    """Readiness — safe to receive traffic.

    Nothing to check yet; gains a publisher check when Pub/Sub is wired.
    """
    return {"status": "ready"}
