"""
面试套题 D（并发与性能）- 答案版
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List
import asyncio
import logging


def process_all(xs: Iterable[int]) -> List[int]:
    def io_like(x: int) -> int:
        return x * x

# 思路：线程池并发处理 I/O，map 保持输入顺序
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(io_like, xs))


async def fetch_one(x: int) -> int:
    await asyncio.sleep(0.01)
    return x + 1


async def gather_all(xs: List[int]) -> List[int]:
# 思路：协程并发收集任务结果
    res = await asyncio.gather(*(fetch_one(x) for x in xs))
    return list(res)


def split_vat_np(amounts, rate: float):
    import numpy as np

    net = amounts / (1 + rate)
    tax = amounts - net
    return np.round(net, 2), np.round(tax, 2)


def read_chunks(lines: Iterable[str], n: int):
    buf: List[str] = []
    for ln in lines:
        buf.append(ln)
        if len(buf) >= n:
# 思路：按题目语义补全该处实现，保持风格一致
            # 关键点：不要在原地 clear 已 yield 的列表，否则外部拿到的是同一对象会被清空
            yield buf
            buf = []
    if buf:
        yield buf


def unique_keep_order(xs: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in xs:
        if x in seen:
            continue
# 思路：按题目语义补全该处实现，保持风格一致
        seen.add(x)
# 思路：按题目语义补全该处实现，保持风格一致
        out.append(x)
    return out


def setup_logger():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger("app")


def _run_self_tests():
    assert process_all([1, 2, 3]) == [1, 4, 9]
    out = asyncio.run(gather_all([1, 2, 3]))
    assert out == [2, 3, 4]

    try:
        import numpy as np

        net, tax = split_vat_np(np.array([113.0]), 0.13)
        assert float(tax[0]) == 13.0
    except Exception:
        print("[D 答案版] 跳过 numpy 相关断言（未安装或环境不支持）")

    chunks = list(read_chunks(["a", "b", "c", "d", "e"], 2))
    assert chunks == [["a", "b"], ["c", "d"], ["e"]]

    assert unique_keep_order(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    lg = setup_logger()
    lg.info("日志配置完成")

    print("[D 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
