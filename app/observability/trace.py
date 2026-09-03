"""Correlates log lines with the Cloud Trace id of the current request.

Cloud Run sets ``X-Cloud-Trace-Context: TRACE_ID/SPAN_ID;o=1``. The trace id is
stored in a context variable so any log line in the call stack picks it up
without threading a request object through every function signature.
"""

from contextvars import ContextVar

_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)

TRACE_HEADER = "X-Cloud-Trace-Context"


def parse_trace_header(header: str | None) -> str | None:
    """Extract the trace id from the Cloud Run trace header."""
    if not header:
        return None
    return header.split("/", 1)[0].strip() or None


def set_trace(trace_id: str | None) -> None:
    _trace_id.set(trace_id)


def current_trace() -> str | None:
    return _trace_id.get()


def formatted_trace(project: str) -> str | None:
    """Cloud Logging requires the fully qualified ``projects/.../traces/...`` form."""
    trace_id = current_trace()
    if not trace_id or not project:
        return None
    return f"projects/{project}/traces/{trace_id}"
