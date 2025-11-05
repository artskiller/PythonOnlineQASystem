"""
面试套题 A（基础与标准库）- 答案版

说明：
- 所有空白已填充，运行本文件将执行自检断言。
"""

from __future__ import annotations

import csv
import os
import re
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Iterable, Iterator, List, Tuple
import io


def extract_amounts(text: str) -> List[float]:
    pattern = re.compile(r"(?:\d+(?:\.\d+)?)")
    return [float(m) for m in pattern.findall(text)]


def sum_by_dept(rows: List[Tuple[str, float]]) -> Dict[str, float]:
    depts = {d for d, _ in rows}
    return {d: sum(v for dd, v in rows if dd == d) for d in depts}


def sort_records(recs: List[Dict]) -> List[Dict]:
    return sorted(
        recs,
        key=lambda r: (
            datetime.strptime(r["date"], "%Y-%m-%d"),
            -r["amount"],
        ),
    )


def clean_lines(lines: Iterable[str]) -> Iterator[str]:
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        yield s.replace("，", ",")


@contextmanager
def temp_chdir(path: str):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def add_tax_amount(rows: Iterable[Dict[str, str]], rate: float):
    for r in rows:
        amt = float(r["amount"])
        tax = round(amt * rate / (1 + rate), 2)
        r["tax"] = f"{tax:.2f}"
        yield r


def process_csv(fin, fout, rate: float):
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames + ["tax"]
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(add_tax_amount(reader, rate))


def _run_self_tests():
    assert extract_amounts("合计: 123, 税额: 45.67 元") == [123.0, 45.67]

    data = [("A", 10), ("B", 5), ("A", 2.5)]
    assert sum_by_dept(data) == {"A": 12.5, "B": 5.0}

    src = [
        {"date": "2024-03-31", "amount": 100.5},
        {"date": "2024-01-01", "amount": 200.0},
        {"date": "2024-03-31", "amount": 80},
    ]
    out = sort_records(src)
    assert [o["amount"] for o in out] == [200.0, 100.5, 80]

    assert list(clean_lines([" a ", "", "b，c"])) == ["a", "b,c"]

    cwd = os.getcwd()
    with temp_chdir(os.path.dirname(__file__)):
        pass
    assert os.getcwd() == cwd

    fin = io.StringIO("amount\n113\n")
    fout = io.StringIO()
    process_csv(fin, fout, 0.13)
    assert fout.getvalue().strip().splitlines() == [
        "amount,tax",
        "113,13.00",
    ]

    print("[A 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

