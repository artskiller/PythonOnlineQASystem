"""
面试套题 J（业务进阶）- 答案版
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import json
import io
import csv
import re


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


def read_filter_jsonl(text: str, period: str) -> List[Dict]:
    out: List[Dict] = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        if obj.get("period") == period:
            out.append(obj)
    return out


def rate_category(rate: float) -> str:
    if rate in {0.13, 0.09, 0.06, 0.03}:
        return f"VAT{int(rate*100)}"
    return "OTHER"


def export_summary_csv(rows: Iterable[Dict]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["period", "dept", "amount"])
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["period"], r["dept"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])
    for (p, d), v in sorted(acc.items()):
        writer.writerow([p, d, f"{v:.2f}"])
    return buf.getvalue()


def is_valid_usci(code: str) -> bool:
# 思路：按题目语义补全该处实现，保持风格一致
    return re.fullmatch(r"[0-9A-Z]{18}", code) is not None


def rounding_compare(x: str) -> Tuple[str, str]:
    d = Decimal(x)
# 思路：按题目语义补全该处实现，保持风格一致
    bank = d.quantize(Decimal("0.00"), rounding=ROUND_HALF_EVEN)
# 思路：按题目语义补全该处实现，保持风格一致
    halfup = d.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    return (str(bank), str(halfup))


def _run_self_tests():
    rows = [
        {"code": "c", "number": "n", "amount": 100.00},
        {"code": "c", "number": "n", "amount": 100.005},
        {"code": "c", "number": "n", "amount": 100.03},
    ]
    out = dedupe_invoices(rows)
    assert len(out) == 2

    text = "\n".join([
        json.dumps({"period": "2024-03", "v": 1}),
        json.dumps({"period": "2024-04", "v": 2}),
    ])
    got = read_filter_jsonl(text, "2024-03")
    assert len(got) == 1 and got[0]["v"] == 1

    assert rate_category(0.13) == "VAT13" and rate_category(0.07) == "OTHER"

    csv_text = export_summary_csv([
        {"period": "2024-03", "dept": "A", "amount": 10},
        {"period": "2024-03", "dept": "A", "amount": 2},
        {"period": "2024-03", "dept": "B", "amount": 5},
    ])
    assert "2024-03,A,12.00" in csv_text and "2024-03,B,5.00" in csv_text

    assert is_valid_usci("91350100M0001XU43T") is True
    assert is_valid_usci("91350100M0001XU43") is False
    assert is_valid_usci("91350100m0001XU43A") is False

    bank, up = rounding_compare("2.345")
    assert bank == "2.34" and up == "2.35"

    print("[J 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
