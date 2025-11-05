"""
面试套题 T（异步任务编排专项）- 空白版

题型：实现题（asyncio）
- 任务去重（按 key）
- 队列与背压（最大队列长度）
- 重试与退避（带抖动）
- 优雅关闭
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
        # TODO：启动后台 worker
        pass

    async def close(self) -> None:
        # TODO：优雅关闭：等待队列清空并取消 worker
        pass

    async def submit(self, key: str, coro_factory: Callable[[], Awaitable[Any]]) -> bool:
        """提交任务；若 key 已在队列或执行中，则返回 False（去重）"""
        # TODO：实现去重与队列放入
        return True

    async def _run(self):
        while True:
            key, fn = await self.queue.get()
            try:
                # TODO：带重试与指数退避（含抖动 0~10ms）
                pass
            finally:
                self._keys_inflight.discard(key)
                self.queue.task_done()


async def _run_self_tests():
    tm = TaskManager(maxsize=2, retries=2)
    await tm.start()

    seen: list[int] = []

    async def work(x: int):
        await asyncio.sleep(0.005)
        seen.append(x)
        return x

    # 去重：相同 key 只保留一次
    ok1 = await tm.submit("k1", lambda: work(1))
    ok2 = await tm.submit("k1", lambda: work(99))
    assert ok1 is True and ok2 is False

    # 背压：队列满时等待（这里不易精确断言，提交后关闭等待）
    await tm.submit("k2", lambda: work(2))
    await tm.submit("k3", lambda: work(3))

    # 重试：第一次失败后成功
    calls = {"n": 0}

    async def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("boom")
        return 42

    await tm.submit("k4", flaky)

    await tm.close()
    assert calls["n"] >= 2 and set(seen) >= {1, 2, 3}
    print("[T 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    asyncio.run(_run_self_tests())

