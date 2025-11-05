"""
面试套题 D（并发与性能）- 空白版

涵盖：线程池/asyncio/numpy/生成器分块/去重/日志
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List
import asyncio
import logging


def process_all(xs: Iterable[int]) -> List[int]:
    """线程池并行执行 I/O 类任务，保持输入顺序"""

    def io_like(x: int) -> int:
        return x * x

    with ThreadPoolExecutor(max_workers=____) as ex:  # 填空：如 4
        return list(ex.map(io_like, xs))


async def fetch_one(x: int) -> int:
    await asyncio.sleep(0.01)
    return x + 1


async def gather_all(xs: List[int]) -> List[int]:
    """并发收集每个 fetch 的结果"""
    res = await asyncio.____(*(fetch_one(x) for x in xs))  # 填空：gather
    return list(res)


def split_vat_np(amounts, rate: float):
    """使用 numpy 向量化拆分含税金额。返回 (net, tax)。"""
    import numpy as np

    net = amounts / (1 + rate)
    tax = amounts - net
    return np.round(net, ____), np.round(tax, ____)  # 填空：2, 2


def read_chunks(lines: Iterable[str], n: int):
    """按 n 行分块生成，最后不足 n 的剩余块也会产出"""
    buf: List[str] = []
    for ln in lines:
        buf.append(ln)
        if len(buf) >= n:
            yield ____  # 填空：buf
            buf = []
    if buf:
        yield buf


def unique_keep_order(xs: Iterable[str]) -> List[str]:
    """去重但保持首次出现顺序"""
    seen = set()
    out: List[str] = []
    for x in xs:
        if x in seen:
            continue
        seen.add(____)  # 填空：x
        out.append(____)  # 填空：x
    return out


def setup_logger():
    """配置基础日志：INFO 级别，格式含时间/级别/消息"""
    logging.basicConfig(level=logging.____, format="____ - %(levelname)s - %(message)s")  # 填空：INFO, %(asctime)s
    return logging.getLogger("app")


def _run_self_tests():
    # 1) 线程池
    assert process_all([1, 2, 3]) == [1, 4, 9]

    # 2) asyncio
    out = asyncio.run(gather_all([1, 2, 3]))
    assert out == [2, 3, 4]

    # 3) numpy（若不可用则跳过）
    try:
        import numpy as np

        net, tax = split_vat_np(np.array([113.0]), 0.13)
        assert float(tax[0]) == 13.0
    except Exception as _:
        print("[D 空白版] 跳过 numpy 相关断言（未安装或环境不支持）")

    # 4) 分块
    chunks = list(read_chunks(["a", "b", "c", "d", "e"], 2))
    assert chunks == [["a", "b"], ["c", "d"], ["e"]]

    # 5) 去重保序
    assert unique_keep_order(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    # 6) 日志配置（不做严格断言，仅调用）
    lg = setup_logger()
    lg.info("日志配置完成")

    print("[D 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()
