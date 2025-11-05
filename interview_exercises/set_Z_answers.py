"""
端到端小项目综合题 Z（纯标准库）- 答案版
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, Iterable, List, Tuple


def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    obj = {"ts": datetime.utcnow().isoformat() + "Z", "level": logging.getLevelName(level), "msg": msg}
    obj.update(fields)
    logger.log(level, json.dumps(obj, ensure_ascii=False))


REQUIRED = ("code", "number", "amount", "rate", "date", "dept")


def read_csv_text(text: str) -> List[Dict[str, str]]:
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def validate_row(r: Dict[str, str]) -> Tuple[bool, str]:
    for k in REQUIRED:
        if k not in r or r[k] == "":
            return False, f"missing {k}"
    try:
        float(r["amount"])
        float(r["rate"])
        datetime.strptime(r["date"], "%Y-%m-%d")
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
        out.append({
            **r,
            "amount": amt,
            "rate": rate,
            "net": net,
            "tax": tax,
            "period": dt.strftime("%Y-%m"),
        })
    return out


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute(
        "CREATE TABLE invoices(\n"
        " code TEXT, number TEXT, amount REAL, rate REAL, date TEXT, dept TEXT, net REAL, tax REAL, period TEXT,\n"
        " PRIMARY KEY(code, number)\n"
        ")"
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


def run_pipeline(csv_text: str, logger: logging.Logger) -> str:
    rows = read_csv_text(csv_text)
    log_json(logger, logging.INFO, "ingest_ok", count=len(rows))
    rows2 = transform_rows(rows)
    log_json(logger, logging.INFO, "transform_ok", count=len(rows2))
    con = setup_db()
    persist(con, rows2)
    log_json(logger, logging.INFO, "persist_ok")
    rep = build_report(con)
    log_json(logger, logging.INFO, "report_ok", size=len(rep))
    con.close()
    return rep


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="端到端小项目综合题 Z")
    ap.add_argument("--input", help="CSV 输入文件路径")
    ap.add_argument("--out", help="报表输出路径", default="")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    lg = logging.getLogger("z")

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    rep = run_pipeline(text, lg)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fo:
            fo.write(rep)
    else:
        print(rep)
    return 0


def _run_self_tests():
    csv_text = """code,number,amount,rate,date,dept
001,001,113,0.13,2024-03-01,A
001,002,106,0.06,2024-03-15,A
002,003,113,0.13,2024-04-01,B
""".strip()

    buf = io.StringIO()
    h = logging.StreamHandler(buf)
    h.setLevel(logging.INFO)
    lg = logging.getLogger("ztest")
    lg.handlers[:] = []
    lg.setLevel(logging.INFO)
    lg.addHandler(h)

    rep = run_pipeline(csv_text, lg)
    lines = [ln for ln in rep.strip().splitlines() if ln.strip()]
    assert lines[0].startswith("period,dept,amount_sum,tax_sum")
    assert any(ln.startswith("2024-03,A,219.0,19.0") for ln in lines)
    assert any(ln.startswith("2024-04,B,113.0,13.0") for ln in lines)

    logs = buf.getvalue().strip().splitlines()
    assert any("ingest_ok" in s for s in logs) and any("report_ok" in s for s in logs)
    print("[Z 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

