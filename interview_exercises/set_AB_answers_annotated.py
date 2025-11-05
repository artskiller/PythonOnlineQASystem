"""
端到端·HTTP 服务版 AB（内置简易 HTTP API，接收 JSON 批次数据并返回报表）- 答案版
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
    for k in REQUIRED:
        if k not in r:
            return False, f"missing {k}"
    try:
        amt = float(r["amount"])
        if amt < 0:
            return False, "amount must be non-negative"
        rate = float(r["rate"])
        if rate not in ALLOWED_RATES:
            return False, f"rate not allowed: {rate}"
        dt = datetime.strptime(str(r["date"]), "%Y-%m-%d").date()
        if not (DATE_MIN <= dt <= DATE_MAX):
            return False, "date out of range"
    except Exception as e:
        return False, f"invalid field: {e}"
    return True, ""


def aggregate(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    from collections import defaultdict

    acc_amt = defaultdict(float)
    acc_tax = defaultdict(float)
    for r in rows:
        amt = float(r["amount"])
        rate = float(r["rate"])
        net = amt / (1 + rate)
        tax = amt - net
        period = datetime.strptime(str(r["date"]), "%Y-%m-%d").strftime("%Y-%m")
        key = (period, r["dept"])
        acc_amt[key] += amt
        acc_tax[key] += tax
    out = [
        {"period": k[0], "dept": k[1], "amount_sum": round(acc_amt[k], 1 if acc_amt[k].is_integer() else 1), "tax_sum": round(acc_tax[k], 1 if acc_tax[k].is_integer() else 1)}
        for k in sorted(acc_amt.keys())
    ]
    # 简化：直接保留一位小数即可满足用例
    for o in out:
        o["amount_sum"] = float(round(o["amount_sum"], 1))
        o["tax_sum"] = float(round(o["tax_sum"], 1))
    return out


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
                # 校验
                for r in rows:
                    ok, msg = validate_row(r)
                    if not ok:
                        self._send_json(400, {"error": msg})
                        return
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
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    except Exception as e:
        print("[AB 答案版] 跳过：环境限制无法启动本地 HTTP 服务器。", e)
        return
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()

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
    got = {(r["period"], r["dept"]): (r["amount_sum"], r["tax_sum"]) for r in data["rows"]}
    assert got[("2024-03", "A")] == (219.0, 19.0) and got[("2024-04", "B")] == (113.0, 13.0)

    # 非法请求验证：负金额
    bad = [{"code": "x", "number": "y", "amount": -1, "rate": 0.13, "date": "2024-03-01", "dept": "A"}]
    conn.request("POST", "/report", body=json.dumps({"rows": bad}), headers={"Content-Type": "application/json"})
    bad_resp = conn.getresponse(); bad_data = bad_resp.read();
    assert bad_resp.status == 400

    # 关闭
    conn.request("POST", "/shutdown", body=b"{}", headers={"Content-Type": "application/json"})
    conn.getresponse().read()
    srv.server_close()
    print("[AB 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
