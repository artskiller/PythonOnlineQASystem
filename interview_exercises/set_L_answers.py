"""
面试套题 L（调试与修复）- 答案版
"""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Tuple
import os


def merge_dicts(a: Dict, b: Dict) -> Dict:
    c = dict(a)
    c.update(b)
    return c


def join_path(root: str, *parts: str) -> str:
    return os.path.join(root, *parts)


def chunk(xs: List[int], n: int) -> List[List[int]]:
    out = []
    for i in range(0, len(xs), n):
        out.append(xs[i : i + n])
    return out


def setup_logger(name: str = "app") -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(name)


def _run_self_tests():
    a = {"x": 1}; b = {"x": 2, "y": 3}
    c = merge_dicts(a, b)
    assert c == {"x": 2, "y": 3} and a == {"x": 1} and b == {"x": 2, "y": 3}

    p = join_path("/root", "a", "b")
    assert p.endswith(os.path.join("a", "b")) and p.startswith("/root")

    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    lg = setup_logger()
    lg.info("hello")

    print("[L 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

