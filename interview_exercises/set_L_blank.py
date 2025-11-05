"""
面试套题 L（调试与修复）- 空白版

题型包含：修复 Bug、边界处理、日志配置与小型重构
"""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Tuple
import os


# 修复题 L1：字典合并
# 预期：返回 a 与 b 合并后的新字典（b 覆盖 a），且不修改原字典
def merge_dicts(a: Dict, b: Dict) -> Dict:
    c = a  # BUG：应创建副本
    c.update(b)  # OK：但此处会修改 a
    return c


# 修复题 L2：路径拼接（确保跨平台、避免多余分隔）
def join_path(root: str, *parts: str) -> str:
    # BUG：直接拼接
    return root + "/" + "/".join(parts)


# 修复题 L3：切分分块（每块最大 n，最后不足 n 也返回）
def chunk(xs: List[int], n: int) -> List[List[int]]:
    out = []
    i = 0
    while i < len(xs):
        out.append(xs[i : i + n])
        i += n
    return out


# 修复题 L4：日志配置（INFO 级别，格式包含时间/级别/消息）
def setup_logger(name: str = "app") -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")  # BUG：级别与格式不符合
    return logging.getLogger(name)


def _run_self_tests():
    # L1
    a = {"x": 1}; b = {"x": 2, "y": 3}
    c = merge_dicts(a, b)
    assert c == {"x": 2, "y": 3} and a == {"x": 1} and b == {"x": 2, "y": 3}

    # L2
    p = join_path("/root", "a", "b")
    assert p.endswith(os.path.join("a", "b")) and p.startswith("/root")

    # L3
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    # L4（不严格断言日志内容，仅调用）
    lg = setup_logger()
    lg.info("hello")

    print("[L 空白版] 自检断言：全部通过（修复上述函数以通过断言）")


if __name__ == "__main__":
    _run_self_tests()

