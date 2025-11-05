"""
面试套题 Q（数据脱敏与合规专项）- 答案版
"""

from __future__ import annotations

import hashlib
import re
from typing import Dict, Iterable, List


def hash_with_salt(text: str, salt: str) -> str:
    h = hashlib.sha256()
    h.update((salt + text).encode("utf-8"))
    return h.hexdigest()


def mask_name(name: str) -> str:
    if not name:
        return name
    if len(name) <= 2:
        return name[0] + "*" * (len(name) - 1)
    return name[0] + "*" * (len(name) - 2) + name[-1]


def mask_email(email: str) -> str:
    m = re.match(r"^([^@]+)@(.+)$", email)
    if not m:
        return email
    local, domain = m.group(1), m.group(2)
    if not local:
        return email
    return local[0] + "*" * max(1, len(local) - 1) + "@" + domain


def check_k_anonymity(rows: Iterable[Dict], quasi_keys: List[str], k: int) -> bool:
    from collections import Counter

    cnt = Counter()
    for r in rows:
        key = tuple(r.get(q) for q in quasi_keys)
        cnt[key] += 1
    return all(v >= k for v in cnt.values()) if cnt else True


def looks_like_cn_id(s: str) -> bool:
    return re.fullmatch(r"\d{17}[0-9X]", s) is not None


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

    print("[Q 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

