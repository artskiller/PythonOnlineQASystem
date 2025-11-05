"""
专项套题 V（OCR 文本清洗与字段抽取，模拟）- 空白版

不依赖 OCR 库，给定“识别后文本”的字符串，完成：
- 规范化文本：标点/货币符号/常见误识别（O->0 等）
- 提取字段：发票代码 code、发票号码 number、金额 amount
"""

from __future__ import annotations

import re
from typing import Dict


def normalize_text(s: str) -> str:
    """规范化 OCR 文本：
    - 全角标点转半角：，：-> , :
    - 货币符号统一为 ¥
    - 常见误识别：字母 O 与 数字 0 的替换（仅在数字块内）
    - 统一标签：发票号/发票号码/票号 -> 发票号；纳税识别号/税号 -> 税号
    """
    # TODO：实现
    return s


LINE_RE = re.compile(r"发票号[:：]?(?P<number>\d{8,12}).*?代码[:：]?(?P<code>\d{10,12}).*?金额[:：]?(?P<amt>\d+(?:\.\d+)?)", re.S)


def extract_fields(s: str) -> Dict[str, str]:
    """从清洗后的文本中提取 code/number/amount"""
    m = LINE_RE.search(s)
    if not m:
        return {}
    d = m.groupdict()
    return {"code": d.get("code", ""), "number": d.get("number", ""), "amount": d.get("amt", "")}


def _run_self_tests():
    raw = """
    金额：RMB 113.OO
    票号: 12345678  税号: 91350100M0001XU43T
    代 码： 044031900111
    """.strip()
    s = normalize_text(raw)
    got = extract_fields(s)
    assert got["number"] == "12345678" and got["code"] == "044031900111" and got["amount"] in {"113.00", "113.0"}
    print("[V 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

