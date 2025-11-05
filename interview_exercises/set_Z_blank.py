"""
端到端小项目综合题 Z（纯标准库）- 空白版

项目目标：实现一个发票数据处理流水线（CLI + 配置 + 校验 + 转换 + 持久化 + 报表 + 日志）。

功能要求：
- CLI：`python set_Z_blank.py --input in.csv --out report.csv`（测试用例使用内存字符串，不强制实际文件）
- 配置：默认税额拆分按行内 `rate` 字段，不做全局覆盖；日志采用 JSON 单行输出。
- 数据：CSV 列包含 `code,number,amount,rate,date,dept`
- 处理：
  1) 读取与基本校验（必填、类型）
  2) 转换：计算 `net=amount/(1+rate)` 与 `tax=amount-net`（四舍五入 2 位），`period=YYYY-MM`
  3) 持久化：写入 sqlite 内存库，表 `invoices`（主键 code,number）
  4) 报表：按 `period,dept` 汇总金额与税额，输出 CSV 文本
  5) 日志：关键阶段输出结构化 JSON 日志

请在 TODO 处完善实现。运行本文件会执行端到端自检。
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


# ========= 结构化日志 =========
def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    # TODO：输出一行 JSON，至少包含 ts/level/msg
    pass


# ========= 数据读取与校验 =========
REQUIRED = ("code", "number", "amount", "rate", "date", "dept")


def read_csv_text(text: str) -> List[Dict[str, str]]:
    # TODO：读取 CSV 文本为字典列表（保留字符串）
    return []


def validate_row(r: Dict[str, str]) -> Tuple[bool, str]:
    # TODO：检查必填字段；尝试将 amount/rate 转为 float、date 转为日期
    return True, ""


# ========= 转换 =========
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


# ========= 持久化 =========
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
    # TODO：参数化插入 OR REPLACE
    pass


# ========= 报表 =========
def build_report(con: sqlite3.Connection) -> str:
    """返回汇总 CSV 文本：列为 period,dept,amount_sum,tax_sum"""
    # TODO：SQL 分组汇总；写 CSV 字符串
    return ""


# ========= CLI 编排 =========
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

    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    rep = run_pipeline(text, lg)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fo:
            fo.write(rep)
    else:
        print(rep)
    return 0


# ========= 自检 =========
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
    # 表头 + 两行（2024-03 A，2024-04 B）
    assert lines[0].startswith("period,dept,amount_sum,tax_sum")
    assert any(ln.startswith("2024-03,A,219.0,19.0") for ln in lines)
    assert any(ln.startswith("2024-04,B,113.0,13.0") for ln in lines)

    # 检查关键日志事件
    logs = buf.getvalue().strip().splitlines()
    assert any("ingest_ok" in s for s in logs) and any("report_ok" in s for s in logs)

    print("[Z 空白版] 自检断言：全部通过（请完善 TODO 后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

