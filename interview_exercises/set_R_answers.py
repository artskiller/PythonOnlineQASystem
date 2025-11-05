"""
面试套题 R（SQLite 与 SQL 安全）- 答案版
"""

from __future__ import annotations

import sqlite3
from typing import Iterable, List, Tuple, Dict


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE invoices(code TEXT, number TEXT, amount REAL, PRIMARY KEY(code, number))")
    cur.execute("CREATE TABLE org(code TEXT, number TEXT, dept TEXT)")
    con.commit()
    return con


def insert_invoices(con: sqlite3.Connection, rows: Iterable[Tuple[str, str, float]]) -> None:
    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO invoices(code, number, amount) VALUES(?,?,?)", list(rows))
    con.commit()


def insert_org(con: sqlite3.Connection, rows: Iterable[Tuple[str, str, str]]) -> None:
    cur = con.cursor()
    cur.executemany("INSERT INTO org(code, number, dept) VALUES(?,?,?)", list(rows))
    con.commit()


def sum_by_dept(con: sqlite3.Connection) -> Dict[str, float]:
    cur = con.cursor()
    sql = (
        "SELECT IFNULL(o.dept, 'UNK') AS dept, SUM(i.amount) AS total "
        "FROM invoices i LEFT JOIN org o ON i.code=o.code AND i.number=o.number "
        "GROUP BY dept ORDER BY dept"
    )
    res: Dict[str, float] = {}
    for dept, total in cur.execute(sql):
        res[dept] = float(total or 0.0)
    return res


def find_invoice_safe(con: sqlite3.Connection, code: str, number: str):
    cur = con.cursor()
    cur.execute("SELECT amount FROM invoices WHERE code=? AND number=?", (code, number))
    row = cur.fetchone()
    return None if row is None else float(row[0])


def _run_self_tests():
    con = setup_db()
    insert_invoices(con, [("c1", "n1", 100.0), ("c1", "n1", 200.0), ("c2", "n2", 50.0)])
    insert_org(con, [("c1", "n1", "A")])
    agg = sum_by_dept(con)
    assert agg == {"A": 100.0, "UNK": 50.0}

    evil = "n1' OR '1'='1"
    res = find_invoice_safe(con, "c1", evil)
    assert res is None

    print("[R 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

