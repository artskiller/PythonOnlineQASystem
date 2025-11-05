"""
面试套题 M（设计与文档）- 答案版
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Iterable, List


@dataclass(order=True)
class Transaction:
    sort_currency: str = field(init=False, repr=False, compare=True)
    sort_amount: Decimal = field(init=False, repr=False, compare=True)

    tid: str
    amount: Decimal
    currency: str

    def __post_init__(self):
        assert self.amount >= 0, "amount 必须非负"
        assert self.currency in {"CNY", "USD", "EUR"}, "不支持的币种"
        # 排序键：currency 升序、amount 降序
        self.sort_currency = self.currency
        self.sort_amount = Decimal(-1) * self.amount


def aggregate_amounts(rows: Iterable[Transaction]) -> Dict[str, Decimal]:
    acc: Dict[str, Decimal] = {}
    for t in rows:
        acc[t.currency] = acc.get(t.currency, Decimal("0")) + t.amount
    return acc


M3_ANSWER = "B"


def generate_doc() -> str:
    return "本接口要求幂等处理，明确输入输出边界与异常策略。"


def _run_self_tests():
    rows = [
        Transaction("t1", Decimal("10.00"), "CNY"),
        Transaction("t2", Decimal("5.00"), "USD"),
        Transaction("t3", Decimal("7.00"), "CNY"),
    ]
    out = sorted(rows)
    assert [x.tid for x in out] == ["t1", "t3", "t2"]
    agg = aggregate_amounts(rows)
    assert agg == {"CNY": Decimal("17.00"), "USD": Decimal("5.00")}
    assert M3_ANSWER == "B"
    doc = generate_doc()
    assert "幂等" in doc and "边界" in doc
    print("[M 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
