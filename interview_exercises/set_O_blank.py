"""
面试套题 O（算法与实战）- 空白版

题型包含：最短路（网格 BFS）、日志解析与统计、令牌化与清洗、JSON 结构变换
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Tuple
import json
import re


# O1：在 0/1 矩阵网格中从起点到终点的最短步数（4 邻接，1 表示障碍）
def shortest_path(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> int:
    # TODO：BFS 实现；无法到达返回 -1
    return -1


# O2：解析日志行，格式 "level=INFO ts=2024-01-01 msg=hello"，统计各 level 次数
def count_levels(lines: Iterable[str]) -> Dict[str, int]:
    # TODO：正则提取 level 值，大小写一致化
    return {}


# O3：令牌化文本，仅保留字母数字与中文，转小写，按空白切分
def tokenize(text: str) -> List[str]:
    # TODO：将非 [a-zA-Z0-9\u4e00-\u9fff\s] 替换为空格，再 split
    return []


# O4：将平铺 JSON 数组转为字典按某键分组
def group_by_key(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    out: Dict[str, List[Dict]] = {}
    for obj in items:
        k = str(obj.get(key, ""))
        out.setdefault(k, []).append(obj)
    return out


def _run_self_tests():
    # O1
    grid = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0],
    ]
    assert shortest_path(grid, (0, 0), (2, 2)) == 4

    # O2
    logs = [
        "level=info ts=... msg=hi",
        "level=INFO ts=... msg=ok",
        "level=warn ts=... msg=...",
    ]
    cnt = count_levels(logs)
    assert cnt == {"INFO": 2, "WARN": 1}

    # O3
    assert tokenize("Hello，世界! 100%") == ["hello", "世界", "100"]

    # O4
    items = [
        {"dept": "A", "v": 1},
        {"dept": "B", "v": 2},
        {"dept": "A", "v": 3},
    ]
    g = group_by_key(items, "dept")
    assert list(g.keys()) == ["A", "B"] and [x["v"] for x in g["A"]] == [1, 3]

    print("[O 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

