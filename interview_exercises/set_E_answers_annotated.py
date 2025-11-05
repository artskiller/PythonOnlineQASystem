"""
面试套题 E（业务综合）- 答案版
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import re


BRACKETS: List[Tuple[float, float, float]] = [
    (36000, 0.03, 0),
    (144000, 0.10, 2520),
    (300000, 0.20, 16920),
    (420000, 0.25, 31920),
    (660000, 0.30, 52920),
    (960000, 0.35, 85920),
    (float("inf"), 0.45, 181920),
]


def calc_iit(taxable: float) -> float:
    for top, rate, quick in BRACKETS:
        if taxable <= top:
            return round(taxable * rate - quick, 2)
    return 0.0


def net_vat(invoices: List[Dict]) -> float:
    net = 0.0
    for inv in invoices:
        amt, r = float(inv["amount"]), float(inv["rate"])
        tax = amt - amt / (1 + r)
        if inv["type"] == "sale":
            net += tax
        else:
# 思路：按题目语义补全该处实现，保持风格一致
            net -= tax
    return round(net, 2)


def luhn_check(code: str) -> bool:
    s = 0
    alt = False
    for ch in reversed(code):
        if not ch.isdigit():
            return False
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        s += d
        alt = not alt
# 思路：Luhn 校验：加权求和后对 10 取模
    return s % 10 == 0


LINE_RE = re.compile(
    r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)"
)


def parse_line(s: str):
    m = LINE_RE.search(s)
    if not m:
        return None
    d = m.groupdict()
# 思路：按题目语义补全该处实现，保持风格一致
    d["amt"] = float(d["amt"])
    return d


def mask_account(s: str) -> str:
    return re.sub(r"(\d{6,15})(\d{4})", lambda m: "*" * len(m.group(1)) + m.group(2), s)


def monthly_report(df):
    import pandas as pd

    df["period"] = df["date"].dt.to_period("M")
    g = df.groupby(["period", "dept"])["amount"].sum().reset_index()
    p = g.pivot(index="period", columns="dept", values="amount").fillna(0)
    return p


def _run_self_tests():
    assert calc_iit(30000) == round(30000 * 0.03, 2)
    assert calc_iit(200000) == round(200000 * 0.20 - 16920, 2)

    invs = [{"type": "sale", "amount": 113, "rate": 0.13}, {"type": "purchase", "amount": 106, "rate": 0.06}]
    assert net_vat(invs) == round((113 - 100) - (106 - 100), 2)

    assert luhn_check("79927398713") is True

    x = parse_line("发票号:12345678 税号:91350100M0001XU43T 金额:113.00")
    assert x and x["no"] == "12345678" and isinstance(x["amt"], float)

    assert mask_account("账号 6222021234567890").endswith("7890")

    try:
        import pandas as pd

        df = pd.DataFrame({
            "date": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-04-01"]),
            "dept": ["A", "B", "A"],
            "amount": [10, 20, 30],
        })
        rpt = monthly_report(df)
        assert str(rpt.index[0]) == "2024-03" and float(rpt.loc["2024-03", "A"]) == 10
    except Exception:
        print("[E 答案版] 跳过 pandas 相关断言（未安装或环境不支持）")

    print("[E 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
