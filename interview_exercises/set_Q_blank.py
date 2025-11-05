"""
面试套题 Q（数据脱敏与合规专项）- 空白版

题型：实现题
- 哈希+盐
- 姓名/邮箱脱敏
- k-匿名性检查
- 身份号正则检测（简化）
"""

from __future__ import annotations

import hashlib
import re
from typing import Dict, Iterable, List


def hash_with_salt(text: str, salt: str) -> str:
    """返回 sha256(salt + text) 的 16 进制字符串"""
    # TODO：实现
    return ""


def mask_name(name: str) -> str:
    """中文姓名脱敏：保留首尾字符，中间用*号；长度<=2 时仅保留首字符"""
    # TODO：实现
    return name


def mask_email(email: str) -> str:
    """邮箱脱敏：姓名部分保留首字符，其他替换为 *，域名不变"""
    # 例如: alice@example.com -> a****@example.com
    # TODO：实现
    return email


def check_k_anonymity(rows: Iterable[Dict], quasi_keys: List[str], k: int) -> bool:
    """检查是否满足 k-匿名：每个 quasi_keys 分组的记录数 >= k"""
    # TODO：实现
    return True


def looks_like_cn_id(s: str) -> bool:
    """简化版中国身份证：18 位，前 17 位数字，最后一位为数字或大写 X"""
    # TODO：实现
    return False


def _run_self_tests():
    assert hash_with_salt("abc", "x") == hashlib.sha256(b"xabc").hexdigest()
    assert mask_name("张三丰") == "张*丰" and mask_name("李四") == "李*"
    assert mask_email("alice@example.com").startswith("a****@example.com")

    rows = [
        {"dept": "A", "city": "BJ", "age": 30},
        {"dept": "A", "city": "BJ", "age": 31},
        {"dept": "B", "city": "SH", "age": 29},
        {"dept": "B", "city": "SH", "age": 28},
    ]
    assert check_k_anonymity(rows, ["dept", "city"], 2) is True
    assert check_k_anonymity(rows, ["dept", "city"], 3) is False

    assert looks_like_cn_id("11010519491231002X") is True
    assert looks_like_cn_id("11010519491231002x") is False
    assert looks_like_cn_id("123") is False

    print("[Q 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

