"""
面试套题 S（API 设计与契约测试，纯标准库）- 答案版
"""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple
from urllib.parse import parse_qs


def _bad_request(msg: str):
    return 400, {"Content-Type": "application/json"}, {"error": msg}


def handle_request(method: str, path: str, query: str, body: str) -> Tuple[int, Dict[str, str], Dict[str, Any]]:
    headers = {"Content-Type": "application/json"}

    if method == "GET" and path == "/ping":
        return 200, headers, {"pong": True}

    if method == "GET" and path == "/add":
        q = parse_qs(query, keep_blank_values=True)
        try:
            a = int(q.get("a", [None])[0])
            b = int(q.get("b", [None])[0])
        except Exception:
            return _bad_request("invalid parameters")
        if a is None or b is None:
            return _bad_request("missing parameters")
        return 200, headers, {"sum": a + b}

    if method == "POST" and path == "/split_tax":
        try:
            obj = json.loads(body or "{}")
            amount = float(obj["amount"])  # may raise
            rate = float(obj["rate"])     # may raise
        except Exception:
            return _bad_request("invalid json body")
        net = amount / (1 + rate)
        tax = amount - net
        return 200, headers, {"net": round(net, 2), "tax": round(tax, 2)}

    return 404, headers, {"error": "not found"}


def _run_self_tests():
    st, hd, bj = handle_request("GET", "/ping", "", "")
    assert st == 200 and bj == {"pong": True}

    st, _, bj = handle_request("GET", "/add", "a=1&b=2", "")
    assert st == 200 and bj["sum"] == 3

    st, _, bj = handle_request("POST", "/split_tax", "", json.dumps({"amount": 113, "rate": 0.13}))
    assert st == 200 and round(bj["tax"], 2) == 13.0

    st, _, bj = handle_request("GET", "/add", "a=x&b=2", "")
    assert st == 400 and "error" in bj

    st, _, _ = handle_request("GET", "/nope", "", "")
    assert st == 404

    print("[S 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

