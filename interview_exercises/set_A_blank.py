"""
面试套题 A（基础与标准库）- 空白版

说明：
- 使用中文注释与命名，按提示在空白处（____）填写代码。
- 运行本文件将执行自检断言，全部通过即为正确。

涵盖：正则/字典推导/排序键/生成器/上下文管理器/CSV 读写
"""

from __future__ import annotations

import csv
import os
import re
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Iterable, Iterator, List, Tuple
import io


# 1) 金额字符串清洗与提取
def extract_amounts(text: str) -> List[float]:
    """从字符串中提取所有金额（整数或小数），返回浮点列表"""
    pattern = re.compile(r"____")  # 填空
    return [float(m) for m in pattern.findall(text)]


# 2) 部门金额汇总（字典推导）
def sum_by_dept(rows: List[Tuple[str, float]]) -> Dict[str, float]:
    """输入记录：(部门, 金额)，输出各部门金额和"""
    depts = {____ for d, _ in rows}  # 填空
    return {d: sum(v for dd, v in rows if ____) for d in depts}  # 填空


# 3) 多键排序：日期升序，金额降序
def sort_records(recs: List[Dict]) -> List[Dict]:
    """rec: {"date":"YYYY-MM-DD","amount":float}，按日期升序、金额降序排序"""
    return sorted(
        recs,
        key=lambda r: (
            ____,  # 填空：datetime.strptime(r["date"], "%Y-%m-%d")
            ____,  # 填空：-r["amount"]
        ),
    )


# 4) 生成器：流式读取与清洗
def clean_lines(lines: Iterable[str]) -> Iterator[str]:
    """去两侧空白，跳过空行，并将中文逗号替换为英文逗号"""
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        yield s.replace(____, ____)  # 填空


# 5) 自定义上下文：临时切换目录
@contextmanager
def temp_chdir(path: str):
    """进入指定目录，退出时恢复原目录"""
    old = os.getcwd()
    os.chdir(____)  # 填空
    try:
        yield
    finally:
        os.chdir(____)  # 填空


# 6) CSV 读取与追加列
def add_tax_amount(rows: Iterable[Dict[str, str]], rate: float):
    """输入行包含含税金额 amount，新增税额 tax（四舍五入两位）"""
    for r in rows:
        amt = float(r["amount"])
        tax = round(amt * rate / (1 + rate), 2)
        r["tax"] = f"{tax:.2f}"
        yield r


def process_csv(fin, fout, rate: float):
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames + [____]  # 填空：新增列名
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(add_tax_amount(reader, rate))


def _run_self_tests():
    # 1)
    assert extract_amounts("合计: 123, 税额: 45.67 元") == [123.0, 45.67]

    # 2)
    data = [("A", 10), ("B", 5), ("A", 2.5)]
    assert sum_by_dept(data) == {"A": 12.5, "B": 5.0}

    # 3)
    src = [
        {"date": "2024-03-31", "amount": 100.5},
        {"date": "2024-01-01", "amount": 200.0},
        {"date": "2024-03-31", "amount": 80},
    ]
    out = sort_records(src)
    assert [o["amount"] for o in out] == [200.0, 100.5, 80]

    # 4)
    assert list(clean_lines([" a ", "", "b，c"])) == ["a", "b,c"]

    # 5)
    cwd = os.getcwd()
    with temp_chdir(os.path.dirname(__file__)):
        pass
    assert os.getcwd() == cwd

    # 6)
    fin = io.StringIO("amount\n113\n")
    fout = io.StringIO()
    process_csv(fin, fout, 0.13)
    assert fout.getvalue().strip().splitlines() == [
        "amount,tax",
        "113,13.00",
    ]

    print("[A 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

