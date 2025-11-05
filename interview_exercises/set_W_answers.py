"""
专项套题 W（批量数据导入流水线：校验→落库→回执）- 答案版
"""

from __future__ import annotations

import sqlite3
from typing import Dict, Iterable, List, Tuple


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE invoices(code TEXT, number TEXT, amount REAL, PRIMARY KEY(code, number))")
    return con


def validate_row(row: Dict) -> Tuple[bool, str]:
    for k in ("code", "number", "amount"):
        if k not in row:
            return False, f"missing {k}"
    try:
        float(row["amount"])
    except Exception:
        return False, "amount not numeric"
    return True, ""


def import_rows(rows: Iterable[Dict]) -> Dict[str, object]:
    con = setup_db()
    ok = 0
    fail = 0
    errors: List[str] = []
    cur = con.cursor()
    try:
        cur.execute("BEGIN")
        for r in rows:
            valid, msg = validate_row(r)
            if not valid:
                fail += 1
                errors.append(msg)
                continue
            try:
                cur.execute(
                    "INSERT OR REPLACE INTO invoices(code, number, amount) VALUES(?,?,?)",
                    (r["code"], r["number"], float(r["amount"]))
                )
                ok += 1
            except Exception as e:
                fail += 1
                errors.append(str(e))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
    return {"ok": ok, "fail": fail, "errors": errors}


def _run_self_tests():
    rows = [
        {"code": "c1", "number": "n1", "amount": 113},
        {"code": "c2", "number": "n2", "amount": "x"},
        {"number": "n3", "amount": 1},
    ]
    rep = import_rows(rows)
    assert rep["ok"] == 1 and rep["fail"] == 2 and len(rep["errors"]) == 2
    print("[W 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

