"""
面试套题 P（日志与可观测性专项）- 空白版

题型：实现题 + 判断题
- JSON 结构化日志
- 上下文 request_id 注入
- 采样过滤器
- 耗时装饰器
"""

from __future__ import annotations

import io
import json
import logging
import time
from typing import Any, Dict, Callable
import contextvars


# 上下文 request_id（用于注入到日志）
_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


def set_request_id(rid: str | None) -> None:
    _request_id.set(rid)


def get_request_id() -> str | None:
    return _request_id.get()


# P1：实现结构化日志输出为单行 JSON
def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    """输出一行 JSON，至少包含 ts/level/msg/request_id 字段，额外字段并入根层级。
    要求：
    - ts 使用 time.time() 的浮点秒
    - level 使用 logging.getLevelName(level) 的结果
    - request_id 从上下文变量读取（可为 None）
    """
    # TODO：实现
    pass


# P2：采样过滤器：每 N 条放行 1 条
class SamplingFilter(logging.Filter):
    def __init__(self, n: int = 10) -> None:
        super().__init__()
        self.n = n
        self._i = 0

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        # TODO：实现每 n 条放行一次
        return True


# P3：耗时装饰器：调用被装饰函数并记录 duration_ms 到日志
def measure_duration(logger: logging.Logger) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            # TODO：记录执行耗时并调用 log_json
            return fn(*args, **kwargs)
        return wrapper
    return deco


def _run_self_tests():
    # 准备 logger 与内存流
    stream = io.StringIO()
    logger = logging.getLogger("p_test")
    logger.handlers[:] = []
    h = logging.StreamHandler(stream)
    h.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

    # P1：基本 JSON 日志
    set_request_id("req-1")
    log_json(logger, logging.INFO, "hello", x=1)
    line = stream.getvalue().strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["msg"] == "hello" and obj["request_id"] == "req-1" and obj["x"] == 1 and "ts" in obj

    # P2：采样
    stream.seek(0); stream.truncate(0)
    # 清除采样过滤器，确保后续日志可见
    h.filters.clear()
    h.addFilter(SamplingFilter(3))
    for i in range(10):
        log_json(logger, logging.INFO, "s", i=i)
    lines = [ln for ln in stream.getvalue().splitlines() if ln.strip()]
    assert 3 <= len(lines) <= 4  # 10 条采样 1/3，应约 3~4 条

    # P3：耗时装饰器
    stream.seek(0); stream.truncate(0)
    h.filters.clear()

    @measure_duration(logger)
    def add(a, b):
        time.sleep(0.005)
        return a + b

    assert add(1, 2) == 3
    j = json.loads(stream.getvalue().splitlines()[-1])
    assert j["msg"] == "duration" and j["duration_ms"] >= 5

    print("[P 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()
