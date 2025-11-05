"""
面试套题 K（混合题型-基础综合）- 答案版
"""

from __future__ import annotations

from typing import Dict, List


Q1_ANSWER = "B"
Q2_ANSWER = True


def normalize_phone(s: str) -> str:
    digits = [ch for ch in s if ch.isdigit()]
    num = "".join(digits)
    if len(num) > 11:
        return num[-11:]
    return num


def tricky(xs: List[int]) -> List[int]:
    xs2 = xs[:]
    ys = [i for i in range(3)]
    xs2.extend(ys)
    ys.append(99)
    return xs2


PREDICT = tricky([7])


def parse_kv(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" in s:
            k, v = s.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _run_self_tests():
    assert Q1_ANSWER == "B"
    assert Q2_ANSWER is True
    assert normalize_phone("+86-138 0013 8000") == "13800138000"
    assert normalize_phone("12345") == "12345"
    assert PREDICT == tricky([7])
    txt = """
    # cfg
    a=1
    b = 2
    
    c=hello
    """.strip()
    got = parse_kv(txt)
    assert got == {"a": "1", "b": "2", "c": "hello"}
    print("[K 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

