"""
面试套题 P（日志与可观测性专项）- 答案版
"""

from __future__ import annotations

import io
import json
import logging
import time
from typing import Any, Dict, Callable
import contextvars


_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


def set_request_id(rid: str | None) -> None:
    _request_id.set(rid)


def get_request_id() -> str | None:
    return _request_id.get()


def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    obj: Dict[str, Any] = {
        "ts": time.time(),
        "level": logging.getLevelName(level),
        "msg": msg,
        "request_id": get_request_id(),
    }
    obj.update(fields)
    logger.log(level, json.dumps(obj, ensure_ascii=False))


class SamplingFilter(logging.Filter):
    def __init__(self, n: int = 10) -> None:
        super().__init__()
        self.n = max(1, int(n))
        self._i = 0

    def filter(self, record: logging.LogRecord) -> bool:
        self._i += 1
        return (self._i % self.n) == 0


def measure_duration(logger: logging.Logger) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                dt = (time.perf_counter() - t0) * 1000.0
                log_json(logger, logging.INFO, "duration", duration_ms=round(dt, 3), func=getattr(fn, "__name__", "<fn>"))
        return wrapper
    return deco


def _run_self_tests():
    stream = io.StringIO()
    logger = logging.getLogger("p_test")
    logger.handlers[:] = []
    h = logging.StreamHandler(stream)
    h.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

    set_request_id("req-1")
    log_json(logger, logging.INFO, "hello", x=1)
    obj = json.loads(stream.getvalue().strip().splitlines()[-1])
    assert obj["msg"] == "hello" and obj["request_id"] == "req-1" and obj["x"] == 1 and "ts" in obj

    stream.seek(0); stream.truncate(0)
    # 清除采样过滤器，确保后续日志可见
    h.filters.clear()
    h.addFilter(SamplingFilter(3))
    for i in range(10):
        log_json(logger, logging.INFO, "s", i=i)
    lines = [ln for ln in stream.getvalue().splitlines() if ln.strip()]
    assert 3 <= len(lines) <= 4

    stream.seek(0); stream.truncate(0)
    h.filters.clear()
    @measure_duration(logger)
    def add(a, b):
        time.sleep(0.005)
        return a + b

    assert add(1, 2) == 3
    j = json.loads(stream.getvalue().splitlines()[-1])
    assert j["msg"] == "duration" and j["duration_ms"] >= 5

    print("[P 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
