"""
面试套题 J（业务进阶）- 空白版

涵盖：近似去重、JSON Lines 处理、税率分类、CSV 汇总导出、信用代码校验、舍入口径对比
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import json
import io
import csv
import re


# 1) 发票近似去重（按 code, number 相同且金额差<=0.01 视为重复，保留第一条）
def dedupe_invoices(rows: Iterable[Dict]) -> List[Dict]:
    seen = {}
    out: List[Dict] = []
    for r in rows:
        key = (r["code"], r["number"])
        amt = float(r["amount"])
        if key not in seen or abs(seen[key] - amt) > 0.01:
            seen[key] = amt
            out.append(r)
    return out


# 2) 读取 JSON Lines，过滤 period=YYYY-MM 的记录
def read_filter_jsonl(text: str, period: str) -> List[Dict]:
    out: List[Dict] = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        if obj.get("period") == period:
            out.append(obj)
    return out


# 3) 根据税率分类标签
def rate_category(rate: float) -> str:
    # 例：0.13 -> "VAT13"，其他如 0.06 -> "VAT6"，未知 -> "OTHER"
    if rate in {0.13, 0.09, 0.06, 0.03}:  # 示例
        return f"VAT{int(rate*100)}"
    return "OTHER"


# 4) 汇总导出 CSV（按 period, dept 汇总 amount 求和并写出为 CSV 字符串）
def export_summary_csv(rows: Iterable[Dict]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["period", "dept", "amount"])
    # 填空：按 (period, dept) 聚合 amount 求和后写出
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["period"], r["dept"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])
    for (p, d), v in sorted(acc.items()):
        writer.writerow([p, d, f"{v:.2f}"])
    return buf.getvalue()


# 5) 统一社会信用代码（简化校验：长度18且大写字母数字）
def is_valid_usci(code: str) -> bool:
    return re.fullmatch(r"[0-9A-Z]{18}", ____) is not None  # 填空：code


# 6) 舍入口径对比：银行家舍入 vs 四舍五入
def rounding_compare(x: str) -> Tuple[str, str]:
    d = Decimal(x)
    bank = d.quantize(Decimal("0.00"), rounding=____)       # 填空：ROUND_HALF_EVEN（银行家）
    halfup = d.quantize(Decimal("0.00"), rounding=____)     # 填空：ROUND_HALF_UP
    return (str(bank), str(halfup))


def _run_self_tests():
    # 1)
    rows = [
        {"code": "c", "number": "n", "amount": 100.00},
        {"code": "c", "number": "n", "amount": 100.005},  # 近似重复
        {"code": "c", "number": "n", "amount": 100.03},   # 超出阈值
    ]
    out = dedupe_invoices(rows)
    assert len(out) == 2

    # 2)
    text = "\n".join([
        json.dumps({"period": "2024-03", "v": 1}),
        json.dumps({"period": "2024-04", "v": 2}),
    ])
    got = read_filter_jsonl(text, "2024-03")
    assert len(got) == 1 and got[0]["v"] == 1

    # 3)
    assert rate_category(0.13) == "VAT13" and rate_category(0.07) == "OTHER"

    # 4)
    csv_text = export_summary_csv([
        {"period": "2024-03", "dept": "A", "amount": 10},
        {"period": "2024-03", "dept": "A", "amount": 2},
        {"period": "2024-03", "dept": "B", "amount": 5},
    ])
    assert "2024-03,A,12.00" in csv_text and "2024-03,B,5.00" in csv_text

    # 5)
    assert is_valid_usci("91350100M0001XU43T") is True
    assert is_valid_usci("91350100M0001XU43") is False
    assert is_valid_usci("91350100m0001XU43A") is False

    # 6)
    bank, up = rounding_compare("2.345")
    assert bank == "2.34" and up == "2.35"

    print("[J 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()
