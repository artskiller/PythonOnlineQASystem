"""
面试套题 O（算法与实战）- 答案版
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Tuple
import json
import re


def shortest_path(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> int:
    n, m = len(grid), len(grid[0]) if grid else 0
    sr, sc = start
    gr, gc = goal
    if not (0 <= sr < n and 0 <= sc < m and 0 <= gr < n and 0 <= gc < m):
        return -1
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return -1
    q = deque([(sr, sc, 0)])
    vis = {(sr, sc)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (gr, gc):
            return d
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and (nr, nc) not in vis:
                vis.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1


def count_levels(lines: Iterable[str]) -> Dict[str, int]:
    cnt: Dict[str, int] = {}
    pat = re.compile(r"level=([A-Za-z]+)")
    for ln in lines:
        m = pat.search(ln)
        if not m:
            continue
        lv = m.group(1).upper()
        cnt[lv] = cnt.get(lv, 0) + 1
    return cnt


def tokenize(text: str) -> List[str]:
    s = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff\s]", " ", text)
    s = s.lower()
    toks = [t for t in s.split() if t]
    return toks


def group_by_key(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    out: Dict[str, List[Dict]] = {}
    for obj in items:
        k = str(obj.get(key, ""))
        out.setdefault(k, []).append(obj)
    return out


def _run_self_tests():
    grid = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0],
    ]
    assert shortest_path(grid, (0, 0), (2, 2)) == 4

    logs = [
        "level=info ts=... msg=hi",
        "level=INFO ts=... msg=ok",
        "level=warn ts=... msg=...",
    ]
    cnt = count_levels(logs)
    assert cnt == {"INFO": 2, "WARN": 1}

    assert tokenize("Hello，世界! 100%") == ["hello", "世界", "100"]

    items = [
        {"dept": "A", "v": 1},
        {"dept": "B", "v": 2},
        {"dept": "A", "v": 3},
    ]
    g = group_by_key(items, "dept")
    assert list(g.keys()) == ["A", "B"] and [x["v"] for x in g["A"]] == [1, 3]

    print("[O 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
