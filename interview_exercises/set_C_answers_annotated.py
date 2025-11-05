"""
面试套题 C（算法与 Pythonic）- 答案版
"""

from __future__ import annotations

from collections import OrderedDict, Counter
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Tuple
import heapq
import itertools


@dataclass
class LRU:
    cap: int
    _d: OrderedDict = None

    def __post_init__(self):
        self._d = OrderedDict()

    def get(self, k):
        if k not in self._d:
            return -1
        v = self._d.pop(k)
# 思路：按题目语义补全该处实现，保持风格一致
        self._d[k] = v
        return v

    def put(self, k, v):
        if k in self._d:
            self._d.pop(k)
        elif len(self._d) >= self.cap:
# 思路：按题目语义补全该处实现，保持风格一致
            self._d.popitem(False)
        self._d[k] = v


def topk(words: List[str], k: int) -> List[Tuple[str, int]]:
    cnt = Counter(words)
    heap: List[Tuple[int, str]] = []
    for w, c in cnt.items():
# 思路：小顶堆保留 TopK，键为(频次, 词) 实现稳定选择
        heapq.heappush(heap, (c, w))
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(((w, c) for c, w in heap), key=lambda x: (-x[1], x[0]))


def flatten(xs: Iterable[Any]) -> Iterator[Any]:
    for x in xs:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        else:
            yield x


def lower_bound(a: List[int], t: int) -> int:
# 思路：按题目语义补全该处实现，保持风格一致
    l, r = 0, len(a)
    while l < r:
        m = (l + r) // 2
        if a[m] < t:
            l = m + 1
        else:
            r = m
    return l


def rle(s: str):
# 思路：按相邻分组统计运行长度
    return [(ch, sum(1 for _ in grp)) for ch, grp in itertools.groupby(s)]


@dataclass(order=True)
class Invoice:
    period: str
    amount: float


def _run_self_tests():
    c = LRU(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1

    out = topk(list("aaabbc"), 2)
    assert out == [("a", 3), ("b", 2)]

    assert list(flatten([1, [2, (3, 4)], 5])) == [1, 2, 3, 4, 5]
    assert lower_bound([1, 2, 4, 4, 7], 4) == 2
    assert rle("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]

    rows = [Invoice("2024-03", 100), Invoice("2024-01", 200), Invoice("2024-03", 80)]
    out2 = sorted(rows, key=lambda x: (x.period, -x.amount))
    assert [r.amount for r in out2] == [200, 100, 80]

    print("[C 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

