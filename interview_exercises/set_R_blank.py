"""
面试套题 R（SQLite 与 SQL 安全）- 空白版

题型：实现题（仅标准库 sqlite3）
- 建表、主键、参数化插入
- 左连接汇总
- 防 SQL 注入（参数化）
"""

from __future__ import annotations

import sqlite3
from typing import Iterable, List, Tuple, Dict


def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    # 发票表
    cur.execute("CREATE TABLE invoices(code TEXT, number TEXT, amount REAL, PRIMARY KEY(code, number))")
    # 组织表
    cur.execute("CREATE TABLE org(code TEXT, number TEXT, dept TEXT)")
    con.commit()
    return con


def insert_invoices(con: sqlite3.Connection, rows: Iterable[Tuple[str, str, float]]) -> None:
    """参数化插入；重复主键忽略（不报错）"""
    cur = con.cursor()
    # TODO：使用参数化与 INSERT OR IGNORE
    pass


def insert_org(con: sqlite3.Connection, rows: Iterable[Tuple[str, str, str]]) -> None:
    cur = con.cursor()
    cur.executemany("INSERT INTO org(code, number, dept) VALUES(?,?,?)", list(rows))
    con.commit()


def sum_by_dept(con: sqlite3.Connection) -> Dict[str, float]:
    """左连接 org 映射部门，NULL 记为 'UNK'，返回 {dept: sum_amount}"""
    cur = con.cursor()
    # TODO：编写聚合 SQL（左连接 + IFNULL）
    return {}


def find_invoice_safe(con: sqlite3.Connection, code: str, number: str):
    """参数化查询，防止注入"""
    cur = con.cursor()
    # TODO：参数化 select
    return None


def _run_self_tests():
    con = setup_db()
    insert_invoices(con, [("c1", "n1", 100.0), ("c1", "n1", 200.0), ("c2", "n2", 50.0)])
    insert_org(con, [("c1", "n1", "A")])
    agg = sum_by_dept(con)
    assert agg == {"A": 100.0, "UNK": 50.0}

    # 注入尝试不会破坏查询
    evil = "n1' OR '1'='1"
    res = find_invoice_safe(con, "c1", evil)
    assert res is None

    print("[R 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

