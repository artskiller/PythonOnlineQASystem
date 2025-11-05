"""
面试套题 S（API 设计与契约测试，纯标准库）- 空白版

题型：实现题
- 路由分发（方法+路径）
- 查询参数解析与校验
- JSON 请求体校验与业务处理
- 错误码与错误消息
"""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple
from urllib.parse import parse_qs


def handle_request(method: str, path: str, query: str, body: str) -> Tuple[int, Dict[str, str], Dict[str, Any]]:
    """返回 (status, headers, body_json)；headers 至少含 {'Content-Type':'application/json'}
    路由：
    - GET /ping -> {"pong":true}
    - GET /add?a=1&b=2 -> {"sum":3}
    - POST /split_tax {"amount":113,"rate":0.13} -> {"net":100.0,"tax":13.0}
    错误：
    - 参数缺失/类型错误 -> 400
    - 未知路由 -> 404
    """
    headers = {"Content-Type": "application/json"}
    # TODO：实现
    return 500, headers, {"error": "not implemented"}


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

    print("[S 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

