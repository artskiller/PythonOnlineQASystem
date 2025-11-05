"""
面试套题 M（设计与文档）- 空白版

题型包含：dataclass 设计、类型注解、聚合函数、选择题、文档说明生成
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Iterable, List


# 设计题 M1：实现交易数据类 Transaction
# 要求：
# - 字段：tid(str)、amount(Decimal)、currency(str)
# - 校验：amount >= 0；currency ∈ {"CNY","USD","EUR"}
# - 排序：按 currency 升序，再按 amount 降序
@dataclass(order=True)
class Transaction:
    # TODO：完善字段与 __post_init__ 校验与排序需要的字段顺序
    tid: str = ""
    amount: Decimal = Decimal("0")
    currency: str = "CNY"

    def __post_init__(self):
        pass


# 实现 M2：聚合同币种总额，返回 {currency: Decimal}
def aggregate_amounts(rows: Iterable[Transaction]) -> Dict[str, Decimal]:
    # TODO 实现
    return {}


# 选择题 M3：关于 typing.Protocol 与 ABC，哪项正确？
# A. Protocol 运行时检查实现
# B. Protocol 支持结构化子类型（鸭子类型）
# C. ABC 只能用于函数参数
# D. Protocol 不能定义属性
M3_ANSWER = "__"  # 选择一项


# 文档生成 M4：生成一段说明，至少包含“幂等”和“边界”两个关键词
def generate_doc() -> str:
    # TODO：返回包含关键词的简短说明
    return ""


def _run_self_tests():
    rows = [
        Transaction("t1", Decimal("10.00"), "CNY"),
        Transaction("t2", Decimal("5.00"), "USD"),
        Transaction("t3", Decimal("7.00"), "CNY"),
    ]

    # M1 排序
    out = sorted(rows, key=lambda x: (x.currency, -float(x.amount)))
    assert [x.tid for x in out] == ["t1", "t3", "t2"]

    # M2 聚合
    agg = aggregate_amounts(rows)
    assert agg == {"CNY": Decimal("17.00"), "USD": Decimal("5.00")}

    # M3
    assert M3_ANSWER in {"A", "B", "C", "D"}
    assert M3_ANSWER == "B"

    # M4
    doc = generate_doc()
    assert "幂等" in doc and "边界" in doc

    print("[M 空白版] 自检断言：全部通过（请完善实现与答案）")


if __name__ == "__main__":
    _run_self_tests()
