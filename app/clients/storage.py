from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from app.config import settings


class StorageClient:
    def __init__(self) -> None:
        self._bucket = None
        if settings.gcs_bucket:
            from google.cloud import storage

            client = storage.Client(project=settings.gcp_project or None)
            self._bucket = client.bucket(settings.gcs_bucket)
        self._local_root = Path(settings.local_output_dir)

    def _object_name(self, event_type: str) -> str:
        now = datetime.now(timezone.utc)
        return (
            f"{settings.gcs_prefix}/{event_type}/"
            f"{now:%Y/%m/%d}/{now:%H%M%S}_{uuid.uuid4().hex[:8]}.json"
        )

    def write_json(self, event_type: str, payload: dict) -> str:
        name = self._object_name(event_type)
        body = json.dumps(payload, separators=(",", ":")).encode()
        if self._bucket is None:
            path = self._local_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            return str(path.resolve())

        blob = self._bucket.blob(name)
        blob.upload_from_string(body, content_type="application/json")
        return f"gs://{settings.gcs_bucket}/{name}"

    def list_objects(self, limit: int = 100) -> list[str]:
        if self._bucket is None:
            root = self._local_root / settings.gcs_prefix
            if not root.exists():
                return []
            return [str(p.resolve()) for p in sorted(root.rglob("*.json"))][:limit]

        blobs = self._bucket.list_blobs(
            prefix=f"{settings.gcs_prefix}/",
            max_results=limit,
        )
        return [f"gs://{settings.gcs_bucket}/{blob.name}" for blob in blobs]


@lru_cache(maxsize=1)
def get_storage() -> StorageClient:
    return StorageClient()
