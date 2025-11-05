"""
面试套题 F（文本与高精度）- 空白版

涵盖：Decimal 高精度、正则多行解析、上下文管理、金额格式化、按键聚合、编码校验
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Dict, Iterable, Iterator, List, Tuple
import re


# 1) 使用 Decimal 高精度计算税额并四舍五入两位
def calc_tax_decimal(amount: str, rate: str) -> str:
    """输入为字符串形式的金额与税率，输出两位小数的税额字符串。例如：('113', '0.13') -> '13.00'"""
    a = Decimal(amount)
    r = Decimal(rate)
    tax = a * r / (Decimal(1) + r)
    with localcontext() as ctx:
        ctx.rounding = ____  # 填空：ROUND_HALF_UP
        return str(tax.quantize(Decimal("0.00")))


# 2) 正则多行解析发票文本，提取 no/taxno/amt
LINE_RE = re.compile(r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)")


def parse_multilines(s: str) -> List[Dict[str, str]]:
    """从多行文本中解析多条发票信息"""
    out: List[Dict[str, str]] = []
    for m in LINE_RE.____(s):  # 填空：finditer
        out.append(m.groupdict())
    return out


# 3) 上下文管理：临时设置 Decimal 精度与舍入模式
class decimal_round:
    """示例上下文：进入时设置 rounding 与 prec，退出时恢复"""

    def __init__(self, rounding, prec: int):
        self.rounding = rounding
        self.prec = prec
        self._token = None

    def __enter__(self):
        self._ctx = localcontext()
        self._token = self._ctx.__enter__()
        self._ctx.rounding = ____  # 填空：self.rounding
        self._ctx.prec = ____      # 填空：self.prec
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._ctx.__exit__(exc_type, exc, tb)


# 4) 金额格式化（千分位，两位小数）
def fmt_amount(x: float) -> str:
    # 期望：1234567.8 -> '1,234,567.80'
    return f"{____:,.2f}"  # 填空：x


# 5) 按键聚合：合并相同 (code, number) 的金额求和
def merge_sum(rows: Iterable[Dict[str, float]]) -> List[Dict[str, float]]:
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["code"], r["number"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])  # 累加
    return [{"code": k[0], "number": k[1], "amount": v} for k, v in acc.items()]


# 6) 税号（大写字母数字 15~20 位）校验
def is_valid_taxno(s: str) -> bool:
    return re.fullmatch(r"[A-Z0-9]{15,20}", ____) is not None  # 填空：s


def _run_self_tests():
    # 1)
    assert calc_tax_decimal("113", "0.13") == "13.00"

    # 2)
    ms = parse_multilines("发票号:123 税号:INVALID 金额:1\n发票号:12345678 税号:91350100M0001XU43T 金额:113.00")
    assert ms[-1]["no"] == "12345678"

    # 3)
    with decimal_round(ROUND_HALF_UP, 10):
        # 精度与舍入设置不抛异常即可
        pass

    # 4)
    assert fmt_amount(1234567.8) == "1,234,567.80"

    # 5)
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

    # 6)
    assert is_valid_taxno("91350100M0001XU43T") is True
    assert is_valid_taxno("invalid") is False

    print("[F 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

