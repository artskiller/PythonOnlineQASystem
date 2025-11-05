"""
面试套题 C（算法与 Pythonic）- 空白版

涵盖：LRU/堆/生成器/二分/itertools/dataclass 排序
"""

from __future__ import annotations

from collections import OrderedDict, Counter
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Tuple
import heapq
import itertools


@dataclass
class LRU:
    """基于 OrderedDict 的简易 LRU 缓存"""

    cap: int
    _d: OrderedDict = None

    def __post_init__(self):
        self._d = OrderedDict()

    def get(self, k):
        if k not in self._d:
            return -1
        v = self._d.pop(k)
        self._d[____] = v  # 填空：移动到尾部（最新）
        return v

    def put(self, k, v):
        if k in self._d:
            self._d.pop(k)
        elif len(self._d) >= self.cap:
            self._d.popitem(____)  # 填空：弹出最旧 last=False
        self._d[k] = v


def topk(words: List[str], k: int) -> List[Tuple[str, int]]:
    """返回出现频次前 k 的单词及其频次，频次降序、字典序升序"""
    cnt = Counter(words)
    heap: List[Tuple[int, str]] = []
    for w, c in cnt.items():
        heapq.heappush(heap, (____, w))  # 填空：(c, w)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(((w, c) for c, w in heap), key=lambda x: (-x[1], x[0]))


def flatten(xs: Iterable[Any]) -> Iterator[Any]:
    """扁平化嵌套的 list/tuple，其他类型原样输出"""
    for x in xs:
        if isinstance(x, (list, tuple)):
            ____ flatten(x)  # 填空：yield from
        else:
            yield x


def lower_bound(a: List[int], t: int) -> int:
    """返回第一个 >= t 的索引（上界）"""
    l, r = 0, len(a)
    while l < r:
        m = (l + r) // 2
        if a[m] < t:
            l = m + 1
        else:
            r = ____  # 填空：m
    return l


def rle(s: str):
    """运行长度编码，输出 (字符, 次数) 列表"""
    return [(ch, sum(1 for _ in grp)) for ch, grp in itertools.____(s)]  # 填空 groupby


@dataclass(order=True)
class Invoice:
    """用于排序的示例数据类：按 period 升序，再按 amount 降序"""

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
    out2 = sorted(rows, key=lambda x: (____, ____))  # 填空：x.period, -x.amount
    assert [r.amount for r in out2] == [200, 100, 80]

    print("[C 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

