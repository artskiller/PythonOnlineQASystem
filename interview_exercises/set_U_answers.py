"""
专项套题 U（Tracing/可观测性-OpenTelemetry 风格模拟，纯标准库）- 答案版
"""

from __future__ import annotations

import contextvars
import io
import json
import logging
import time
import uuid
from typing import Any, Dict


_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
_span_stack: contextvars.ContextVar[list[str]] = contextvars.ContextVar("span_stack", default=[])


def current_ids() -> tuple[str | None, str | None]:
    stk = _span_stack.get()
    sid = stk[-1] if stk else None
    return _trace_id.get(), sid


class start_span:
    def __init__(self, name: str):
        self.name = name
        self._token_stk = None
        self._token_tid = None
        self._new_span = None

    def __enter__(self):
        tid = _trace_id.get()
        if tid is None:
            tid = uuid.uuid4().hex
            self._token_tid = _trace_id.set(tid)
        stk = list(_span_stack.get())
        self._new_span = uuid.uuid4().hex
        stk.append(self._new_span)
        self._token_stk = _span_stack.set(stk)
        return self

    def __exit__(self, exc_type, exc, tb):
        stk = list(_span_stack.get())
        if stk and stk[-1] == self._new_span:
            stk.pop()
        _span_stack.set(stk)
        if self._token_tid is not None:
            _trace_id.reset(self._token_tid)
        if self._token_stk is not None:
            _span_stack.reset(self._token_stk)
        return False


def log_event(logger: logging.Logger, name: str, **fields: Any) -> None:
    tid, sid = current_ids()
    obj: Dict[str, Any] = {
        "ts": time.time(),
        "name": name,
        "trace_id": tid,
        "span_id": sid,
    }
    obj.update(fields)
    logger.info(json.dumps(obj, ensure_ascii=False))


def _run_self_tests():
    stream = io.StringIO()
    lg = logging.getLogger("u_test")
    lg.handlers[:] = []
    h = logging.StreamHandler(stream)
    h.setLevel(logging.INFO)
    lg.setLevel(logging.INFO)
    lg.addHandler(h)

    with start_span("root"):
        log_event(lg, "e1", x=1)
        with start_span("child"):
            log_event(lg, "e2", y=2)

    lines = [json.loads(ln) for ln in stream.getvalue().splitlines() if ln.strip()]
    assert len(lines) == 2
    assert lines[0]["name"] == "e1" and lines[1]["name"] == "e2"
    assert lines[0]["trace_id"] == lines[1]["trace_id"]
    assert lines[0]["span_id"] != lines[1]["span_id"]

    print("[U 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

