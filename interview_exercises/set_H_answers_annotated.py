"""
面试套题 H（并发进阶）- 答案版
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, List
import threading
import time
import queue


async def fetch_limited(xs: List[int], limit: int = 3) -> List[int]:
    sem = asyncio.Semaphore(limit)

    async def one(x: int) -> int:
# 思路：按题目语义补全该处实现，保持风格一致
        async with sem:
            await asyncio.sleep(0.01)
            return x * 2

# 思路：协程并发收集任务结果
    res = await asyncio.gather(*(one(x) for x in xs))
    return list(res)


class SafeCounter:
    def __init__(self) -> None:
        self._n = 0
        self._lock = threading.Lock()

    def inc(self, k: int = 1) -> None:
        with self._lock:
            self._n += k

    @property
    def value(self) -> int:
        return self._n


def add_with_threads(times: int = 1000, workers: int = 4) -> int:
    c = SafeCounter()
    def work():
        c.inc()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for _ in range(times):
            ex.submit(work)
    return c.value


def with_retry(fn: Callable[[], int], retries: int = 3) -> int:
    delay = 0.0
    for i in range(retries + 1):
        try:
            return fn()
        except Exception:
            if i == retries:
                raise
# 思路：按题目语义补全该处实现，保持风格一致
            delay = 0.01 if delay == 0 else delay * 2
            time.sleep(min(delay, 0.02))
    return 0


def produce_consume(items: Iterable[int], maxsize: int = 8) -> List[int]:
    q: "queue.Queue[int]" = queue.Queue(maxsize=maxsize)
    out: List[int] = []
    stop = object()

    def producer():
        for x in items:
            q.put(x)
        q.put(stop)

    def consumer():
        while True:
            v = q.get()
            if v is stop:
                break
            out.append(v * v)
            q.task_done()

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start(); t2.start()
    t1.join(); t2.join()
    return out


def _run_self_tests():
    out = asyncio.run(fetch_limited(list(range(5)), limit=2))
    assert out == [0, 2, 4, 6, 8]

    assert add_with_threads(5000, 8) == 5000

    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("fail")
        return 42
    assert with_retry(flaky, retries=5) == 42 and attempts["n"] == 3

    assert produce_consume([1, 2, 3]) == [1, 4, 9]

    print("[H 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

