"""
端到端·并发版 AA（批量文件扫描→多线程解析→集中落库→汇总报表，含错误隔离与重试）- 答案版
"""

from __future__ import annotations

import contextvars
import csv
import io
import json
import logging
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date
from typing import Any, Dict, Iterable, List, Tuple
import tempfile
import uuid


# ===== Trace/Span 上下文 =====
_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
_span_stack: contextvars.ContextVar[list[str]] = contextvars.ContextVar("span_stack", default=[])


class start_span:
    def __init__(self, name: str):
        self.name = name
        self._token_tid = None
        self._token_stk = None
        self._span_id: str | None = None

    def __enter__(self):
        tid = _trace_id.get()
        if tid is None:
            tid = uuid.uuid4().hex
            self._token_tid = _trace_id.set(tid)
        stk = list(_span_stack.get())
        self._span_id = uuid.uuid4().hex
        stk.append(self._span_id)
        self._token_stk = _span_stack.set(stk)
        return self

    def __exit__(self, exc_type, exc, tb):
        stk = list(_span_stack.get())
        if stk and self._span_id == stk[-1]:
            stk.pop()
        _span_stack.set(stk)
        if self._token_tid is not None:
            _trace_id.reset(self._token_tid)
        if self._token_stk is not None:
            _span_stack.reset(self._token_stk)
        return False


def _ids() -> tuple[str | None, str | None]:
    stk = _span_stack.get()
    sid = stk[-1] if stk else None
    return _trace_id.get(), sid


def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    tid, sid = _ids()
    obj = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "level": logging.getLevelName(level),
        "msg": msg,
        "trace_id": tid,
        "span_id": sid,
    }
    obj.update(fields)
    logger.log(level, json.dumps(obj, ensure_ascii=False))


REQUIRED = ("code", "number", "amount", "rate", "date", "dept")
ALLOWED_RATES = {0.13, 0.09, 0.06, 0.03}
DATE_MIN = date(2000, 1, 1)
DATE_MAX = date(2100, 12, 31)


def validate_row(r: Dict[str, str]) -> Tuple[bool, str]:
    for k in REQUIRED:
        if k not in r or r[k] == "":
            return False, f"missing {k}"
    try:
        amt = float(r["amount"])
        if amt < 0:
            return False, "amount must be non-negative"
        rate = float(r["rate"])
        if rate not in ALLOWED_RATES:
            return False, f"rate not allowed: {rate}"
        dt = datetime.strptime(r["date"], "%Y-%m-%d").date()
        if not (DATE_MIN <= dt <= DATE_MAX):
            return False, "date out of range"
    except Exception as e:
        return False, f"invalid field: {e}"
    return True, ""


def transform_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in rows:
        ok, msg = validate_row(r)
        if not ok:
            raise ValueError(msg)
        amt = float(r["amount"])
        rate = float(r["rate"])
        net = round(amt / (1 + rate), 2)
        tax = round(amt - net, 2)
        dt = datetime.strptime(r["date"], "%Y-%m-%d")
        out.append({**r, "amount": amt, "rate": rate, "net": net, "tax": tax, "period": dt.strftime("%Y-%m")})
    return out


def parse_file(path: str) -> List[Dict[str, Any]]:
    with start_span(f"parse:{os.path.basename(path)}"):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [dict(r) for r in reader]
        return transform_rows(rows)


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute(
        "CREATE TABLE invoices( code TEXT, number TEXT, amount REAL, rate REAL, date TEXT, dept TEXT, net REAL, tax REAL, period TEXT, PRIMARY KEY(code,number))"
    )
    return con


def persist(con: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> None:
    cur = con.cursor()
    cur.executemany(
        "INSERT OR REPLACE INTO invoices(code,number,amount,rate,date,dept,net,tax,period) VALUES(?,?,?,?,?,?,?,?,?)",
        [(
            r["code"], r["number"], r["amount"], r["rate"], r["date"], r["dept"], r["net"], r["tax"], r["period"]
        ) for r in rows]
    )
    con.commit()


def build_report(con: sqlite3.Connection) -> str:
    cur = con.cursor()
    sql = (
        "SELECT period, dept, SUM(amount) AS amount_sum, SUM(tax) AS tax_sum "
        "FROM invoices GROUP BY period, dept ORDER BY period, dept"
    )
    rows = list(cur.execute(sql))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["period", "dept", "amount_sum", "tax_sum"])
    for period, dept, amount_sum, tax_sum in rows:
        w.writerow([period, dept, float(amount_sum or 0), float(tax_sum or 0)])
    return buf.getvalue()


def run_pipeline(root: str, logger: logging.Logger, max_workers: int = 4, retries: int = 1) -> str:
    with start_span("root"):
        files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".csv")]
        log_json(logger, logging.INFO, "scan_ok", count=len(files))

        results: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut_map = {ex.submit(parse_file, p): p for p in files}
            for fut in as_completed(fut_map):
                p = fut_map[fut]
                try:
                    rows = fut.result()
                    results.extend(rows)
                    log_json(logger, logging.INFO, "parse_ok", file=os.path.basename(p), rows=len(rows))
                except Exception as e:
                    if retries > 0:
                        try:
                            rows = parse_file(p)
                            results.extend(rows)
                            log_json(logger, logging.INFO, "parse_ok", file=os.path.basename(p), rows=len(rows), retried=True)
                            continue
                        except Exception as e2:
                            log_json(logger, logging.ERROR, "parse_fail", file=os.path.basename(p), error=str(e2))
                    else:
                        log_json(logger, logging.ERROR, "parse_fail", file=os.path.basename(p), error=str(e))

        with start_span("persist"):
            con = setup_db()
            persist(con, results)
            log_json(logger, logging.INFO, "persist_ok", rows=len(results))
            rep = build_report(con)
            log_json(logger, logging.INFO, "report_ok", size=len(rep))
            con.close()
        return rep


def _make_csv(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["code", "number", "amount", "rate", "date", "dept"])
        w.writeheader()
        w.writerows(rows)


def _run_self_tests():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    lg = logging.getLogger("aa")

    with tempfile.TemporaryDirectory() as d:
        _make_csv(os.path.join(d, "a.csv"), [
            {"code": "001", "number": "001", "amount": 113, "rate": 0.13, "date": "2024-03-01", "dept": "A"},
        ])
        with open(os.path.join(d, "bad.csv"), "w", encoding="utf-8") as f:
            f.write("oops")
        _make_csv(os.path.join(d, "b.csv"), [
            {"code": "002", "number": "002", "amount": 106, "rate": 0.06, "date": "2024-03-15", "dept": "A"},
        ])

        rep = run_pipeline(d, lg)
        lines = [ln for ln in rep.strip().splitlines() if ln.strip()]
        assert lines[0].startswith("period,dept,amount_sum,tax_sum")
        assert any(ln.startswith("2024-03,A,219.0,19.0") for ln in lines)

    print("[AA 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()
