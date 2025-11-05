"""
面试套题 F（文本与高精度）- 答案版
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Dict, Iterable, Iterator, List, Tuple
import re


def calc_tax_decimal(amount: str, rate: str) -> str:
    a = Decimal(amount)
    r = Decimal(rate)
    tax = a * r / (Decimal(1) + r)
    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_UP
        return str(tax.quantize(Decimal("0.00")))


LINE_RE = re.compile(r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)")


def parse_multilines(s: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for m in LINE_RE.finditer(s):
        out.append(m.groupdict())
    return out


class decimal_round:
    def __init__(self, rounding, prec: int):
        self.rounding = rounding
        self.prec = prec
        self._token = None

    def __enter__(self):
        # localcontext 返回一个上下文管理器，其 __enter__() 返回 Context 对象
        self._cm = localcontext()
        self._ctx = self._cm.__enter__()
        self._ctx.rounding = self.rounding
        self._ctx.prec = self.prec
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._cm.__exit__(exc_type, exc, tb)


def fmt_amount(x: float) -> str:
    return f"{x:,.2f}"


def merge_sum(rows: Iterable[Dict[str, float]]) -> List[Dict[str, float]]:
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["code"], r["number"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])  # 累加
    return [{"code": k[0], "number": k[1], "amount": v} for k, v in acc.items()]


def is_valid_taxno(s: str) -> bool:
    return re.fullmatch(r"[A-Z0-9]{15,20}", s) is not None


def _run_self_tests():
    assert calc_tax_decimal("113", "0.13") == "13.00"

    ms = parse_multilines("发票号:123 税号:INVALID 金额:1\n发票号:12345678 税号:91350100M0001XU43T 金额:113.00")
    assert ms[-1]["no"] == "12345678"

    with decimal_round(ROUND_HALF_UP, 10):
        pass

    assert fmt_amount(1234567.8) == "1,234,567.80"

    rows = [
        {"code": "c1", "number": "n1", "amount": 10},
        {"code": "c1", "number": "n1", "amount": 2.5},
        {"code": "c2", "number": "n2", "amount": 3},
    ]
    out = merge_sum(rows)
    assert sorted(out, key=lambda x: x["code"]) == [
        {"code": "c1", "number": "n1", "amount": 12.5},
        {"code": "c2", "number": "n2", "amount": 3.0},
    ]

    assert is_valid_taxno("91350100M0001XU43T") is True
    assert is_valid_taxno("invalid") is False

    print("[F 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
