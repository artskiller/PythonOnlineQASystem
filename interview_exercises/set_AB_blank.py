"""
端到端·HTTP 服务版 AB（内置简易 HTTP API，接收 JSON 批次数据并返回报表）- 空白版

要求：
- 使用 http.server 实现 Handler：
  - POST /report：请求体为 {"rows": [...]}，每行包含 code,number,amount,rate,date,dept
  - 返回 JSON {"rows": [{"period":...,"dept":...,"amount_sum":...,"tax_sum":...}, ...]}
- 校验与转换同前（net/tax/period），出错返回 400 和错误信息
- 提供 /shutdown 关闭服务（仅测试使用）
"""

from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, Iterable, List, Tuple
from datetime import datetime, date
import http.client


REQUIRED = ("code", "number", "amount", "rate", "date", "dept")
ALLOWED_RATES = {0.13, 0.09, 0.06, 0.03}
DATE_MIN = date(2000, 1, 1)
DATE_MAX = date(2100, 12, 31)


def validate_row(r: Dict[str, Any]) -> Tuple[bool, str]:
    # TODO：校验必填与类型；新增业务校验：
    # - 金额非负；税率属于 ALLOWED_RATES；日期在 [DATE_MIN, DATE_MAX]
    return True, ""


def aggregate(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # TODO：按 period,dept 汇总 amount 与 tax
    return []


class Handler(BaseHTTPRequestHandler):
    server_shutdown = False

    def _send_json(self, code: int, obj: Dict[str, Any]):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):  # noqa: N802
        if self.path == "/report":
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            try:
                obj = json.loads(body or "{}")
                rows = obj.get("rows", [])
                # TODO：校验与转换 rows（计算 period、net、tax），非法时返回 400
                agg = aggregate(rows)
                self._send_json(200, {"rows": agg})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return
        if self.path == "/shutdown":
            Handler.server_shutdown = True
            self._send_json(200, {"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        self._send_json(404, {"error": "not found"})


def _run_self_tests():
    # 启动服务
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    except Exception as e:
        print("[AB 空白版] 跳过：环境限制无法启动本地 HTTP 服务器。", e)
        return
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()

    # 构造请求
    rows = [
        {"code": "001", "number": "001", "amount": 113, "rate": 0.13, "date": "2024-03-01", "dept": "A"},
        {"code": "002", "number": "002", "amount": 106, "rate": 0.06, "date": "2024-03-15", "dept": "A"},
        {"code": "003", "number": "003", "amount": 113, "rate": 0.13, "date": "2024-04-01", "dept": "B"},
    ]
    conn = http.client.HTTPConnection("127.0.0.1", port)
    conn.request("POST", "/report", body=json.dumps({"rows": rows}), headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    assert resp.status == 200
    data = json.loads(resp.read())
    # 应包含 2024-03/A 与 2024-04/B 两行
    got = {(r["period"], r["dept"]): (r["amount_sum"], r["tax_sum"]) for r in data["rows"]}
    assert got[("2024-03", "A")] == (219.0, 19.0) and got[("2024-04", "B")] == (113.0, 13.0)

    conn.request("POST", "/shutdown", body=b"{}", headers={"Content-Type": "application/json"})
    conn.getresponse().read()
    srv.server_close()
    print("[AB 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()
