"""
专项套题 V（OCR 文本清洗与字段抽取，模拟）- 答案版
"""

from __future__ import annotations

import re
from typing import Dict


def normalize_text(s: str) -> str:
    s = s.replace("，", ",").replace("：", ":")
    s = re.sub(r"\bRMB\b", "¥", s, flags=re.I)
    s = s.replace("票号", "发票号").replace("发票号码", "发票号")
    s = s.replace("纳税识别号", "税号")
    s = s.replace("代 码", "代码")
    # 在数字块内将 O 纠正为 0：例如 113.OO -> 113.00
    def fix_o(m: re.Match) -> str:
        return re.sub(r"O", "0", m.group(0))
    s = re.sub(r"\d[\dO\.]+", fix_o, s)
    # 去多余空格
    s = re.sub(r"\s+", " ", s)
    return s

def extract_fields(s: str) -> Dict[str, str]:
    num_m = re.search(r"发票号[:：]?\s*(\d{8,12})", s)
    code_m = re.search(r"(?:代码|发票代码)[:：]?\s*(\d{10,12})", s)
    amt_m = re.search(r"金额[:：]?\s*(?:[¥￥])?\s*(\d+(?:\.\d+)?)", s)
    return {
        "code": code_m.group(1) if code_m else "",
        "number": num_m.group(1) if num_m else "",
        "amount": amt_m.group(1) if amt_m else "",
    }


def _run_self_tests():
    raw = """
    金额：RMB 113.OO
    票号: 12345678  税号: 91350100M0001XU43T
    代 码： 044031900111
    """.strip()
    s = normalize_text(raw)
    got = extract_fields(s)
    assert got["number"] == "12345678" and got["code"] == "044031900111" and got["amount"] in {"113.00", "113.0"}
    print("[V 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
