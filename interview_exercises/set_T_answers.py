"""
面试套题 T（异步任务编排专项）- 答案版
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Awaitable, Callable, Dict, Set


class TaskManager:
    def __init__(self, maxsize: int = 8, retries: int = 2) -> None:
        self.queue: "asyncio.Queue[tuple[str, Callable[[], Awaitable[Any]]]]" = asyncio.Queue(maxsize=maxsize)
        self.retries = retries
        self._keys_inflight: Set[str] = set()
        self._worker: asyncio.Task | None = None
        self._closed = False

    async def start(self) -> None:
        if self._worker is None:
            self._worker = asyncio.create_task(self._run())

    async def close(self) -> None:
        await self.queue.join()
        if self._worker:
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                pass
            self._worker = None
        self._closed = True

    async def submit(self, key: str, coro_factory: Callable[[], Awaitable[Any]]) -> bool:
        if self._closed:
            return False
        if key in self._keys_inflight:
            return False
        await self.queue.put((key, coro_factory))
        self._keys_inflight.add(key)
        return True

    async def _run(self):
        try:
            while True:
                key, fn = await self.queue.get()
                try:
                    err = None
                    for i in range(self.retries + 1):
                        try:
                            await fn()
                            err = None
                            break
                        except Exception as e:
                            err = e
                            if i == self.retries:
                                break
                            # 指数退避 + 抖动（0~10ms）
                            delay = min(0.02, (0.005 * (2 ** i)) + random.uniform(0, 0.01))
                            await asyncio.sleep(delay)
                    if err:
                        # 可在此处记录日志；题目不要求
                        pass
                finally:
                    self._keys_inflight.discard(key)
                    self.queue.task_done()
        except asyncio.CancelledError:
            return


async def _run_self_tests():
    tm = TaskManager(maxsize=2, retries=2)
    await tm.start()

    seen: list[int] = []

    async def work(x: int):
        await asyncio.sleep(0.005)
        seen.append(x)
        return x

    ok1 = await tm.submit("k1", lambda: work(1))
    ok2 = await tm.submit("k1", lambda: work(99))
    assert ok1 is True and ok2 is False

    await tm.submit("k2", lambda: work(2))
    await tm.submit("k3", lambda: work(3))

    calls = {"n": 0}

    async def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("boom")
        return 42

    await tm.submit("k4", flaky)

    await tm.close()
    assert calls["n"] >= 2 and set(seen) >= {1, 2, 3}
    print("[T 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    asyncio.run(_run_self_tests())

