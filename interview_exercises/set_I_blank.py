"""
面试套题 I（算法进阶）- 空白版

涵盖：Trie 敏感词脱敏、并查集、KMP、滑窗、快速选择、拓扑排序
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
from collections import deque, defaultdict


# 1) Trie 实现敏感词替换（将匹配的词用 * 替换，保持原长度）
class Trie:
    def __init__(self):
        self.next: Dict[str, Dict] = {}
        self.end = False

    def insert(self, word: str):
        node = self
        for ch in word:
            node = node.next.setdefault(ch, Trie())
        node.end = True

    def mask(self, s: str) -> str:
        n = len(s)
        res = list(s)
        for i in range(n):
            node = self
            j = i
            while j < n and s[j] in node.next:
                node = node.next[s[j]]
                j += 1
                if node.end:
                    # 覆盖 i..j-1 为 *
                    for k in range(i, j):
                        res[k] = '*'
        return ''.join(res)


# 2) 并查集（Union-Find）
class UnionFind:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1


# 3) KMP 查找子串首个位置；找不到返回 -1
def kmp_search(text: str, pat: str) -> int:
    if pat == "":
        return 0
    # 构建前缀函数
    pi = [0] * len(pat)
    j = 0
    for i in range(1, len(pat)):
        while j and pat[i] != pat[j]:
            j = pi[j - 1]
        if pat[i] == pat[j]:
            j += 1
        pi[i] = j
    # 匹配
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pat[j]:
            j = pi[j - 1]
        if ch == pat[j]:
            j += 1
            if j == len(pat):
                return i - j + 1
    return -1


# 4) 无重复字符的最长子串长度（滑动窗口）
def length_of_longest_substring(s: str) -> int:
    last = {}
    l = 0
    ans = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            l = last[ch] + 1
        last[ch] = r
        ans = max(ans, r - l + 1)
    return ans


# 5) 第 k 大元素（快速选择，k 从 1 开始）
def kth_largest(nums: List[int], k: int) -> int:
    import random
    target = len(nums) - k

    def select(lo: int, hi: int) -> int:
        if lo == hi:
            return nums[lo]
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        x = nums[hi]
        i = lo
        for j in range(lo, hi):
            if nums[j] <= x:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target:
            return nums[i]
        elif i < target:
            return select(i + 1, hi)
        else:
            return select(lo, i - 1)

    return select(0, len(nums) - 1)


# 6) 拓扑排序（Kahn 算法）。输入边列表，返回一种拓扑序；若有环返回空列表。
def topo_sort(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    indeg = [0] * n
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    out: List[int] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else []


def _run_self_tests():
    t = Trie(); [t.insert(w) for w in ["税务", "发票"]]
    assert t.mask("税务AI处理发票") == "**AI处理**"

    uf = UnionFind(5)
    uf.union(0, 1); uf.union(1, 2)
    assert uf.find(0) == uf.find(2) and uf.find(3) != uf.find(0)

    assert kmp_search("ababcababa", "ababa") == 5
    assert length_of_longest_substring("abcabcbb") == 3
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    order = topo_sort(4, [(0, 1), (1, 2), (0, 3)])
    assert order[:1] == [0] and set(order) == {0, 1, 2, 3}

    print("[I 空白版] 自检断言：全部通过（请根据题意在需要处填写空白再验证）")


if __name__ == "__main__":
    _run_self_tests()

