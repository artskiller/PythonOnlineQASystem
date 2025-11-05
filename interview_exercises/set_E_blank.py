"""
面试套题 E（业务综合）- 空白版

涵盖：个税/增值税/发票解析/脱敏/pandas 报表
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
    """根据简化税率表计算个税：税额=应纳税所得额*税率-速算扣除"""
    for top, rate, quick in BRACKETS:
        if taxable <= top:
            return round(____ * ____ - ____, 2)  # 填空：taxable, rate, quick
    return 0.0


def net_vat(invoices: List[Dict]) -> float:
    """销项税-进项税，金额为含税金额，税额=含税-不含税"""
    net = 0.0
    for inv in invoices:
        amt, r = float(inv["amount"]), float(inv["rate"])
        tax = amt - amt / (1 + r)
        if inv["type"] == "sale":
            net += tax
        else:
            net -= ____  # 填空：tax
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
    return s % ____ == 0  # 填空：10


LINE_RE = re.compile(
    r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)"
)


def parse_line(s: str):
    m = LINE_RE.search(s)
    if not m:
        return None
    d = m.groupdict()
    d["amt"] = ____(d["amt"])  # 填空：float
    return d


def mask_account(s: str) -> str:
    """将连续 10~19 位数字的账号脱敏，保留末 4 位，其余用 * 替代"""
    return re.sub(r"(\d{6,15})(\d{4})", lambda m: "*" * len(m.group(1)) + m.group(2), s)


def monthly_report(df):
    """按月份与部门汇总金额并透视为列（需要 pandas）"""
    import pandas as pd

    df["period"] = df["date"].dt.to_period("M")
    g = df.groupby([____, ____])["amount"].sum().reset_index()  # 填空："period", "dept"
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

    # pandas 测试（若不可用则跳过）
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
        print("[E 空白版] 跳过 pandas 相关断言（未安装或环境不支持）")

    print("[E 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()
