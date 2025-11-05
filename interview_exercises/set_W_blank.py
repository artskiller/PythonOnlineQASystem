"""
专项套题 W（批量数据导入流水线：校验→落库→回执）- 空白版

要求：
- validate_row(row) 校验必填字段：code, number, amount；类型正确
- import_rows(rows) 事务落库（sqlite3 内存库），返回汇总 {ok, fail, errors}
"""

from __future__ import annotations

import sqlite3
from typing import Dict, Iterable, List, Tuple


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE invoices(code TEXT, number TEXT, amount REAL, PRIMARY KEY(code, number))")
    return con


def validate_row(row: Dict) -> Tuple[bool, str]:
    # TODO：检查必填与类型
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
                cur.execute("INSERT OR REPLACE INTO invoices(code, number, amount) VALUES(?,?,?)", (r["code"], r["number"], float(r["amount"])) )
                ok += 1
            except Exception as e:
                fail += 1
                errors.append(str(e))
        con.commit()
    except Exception as e:
        con.rollback()
        raise
    finally:
        con.close()
    return {"ok": ok, "fail": fail, "errors": errors}


def _run_self_tests():
    rows = [
        {"code": "c1", "number": "n1", "amount": 113},
        {"code": "c2", "number": "n2", "amount": "x"},  # 类型错
        {"number": "n3", "amount": 1},  # 缺 code
    ]
    rep = import_rows(rows)
    assert rep["ok"] == 1 and rep["fail"] == 2 and len(rep["errors"]) == 2
    print("[W 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

