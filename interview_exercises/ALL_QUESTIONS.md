# 面试套题汇总（空白题）

## 目录
- [set_AA_blank.py](#set_AA_blank)
- [set_AB_blank.py](#set_AB_blank)
- [set_A_blank.py](#set_A_blank)
- [set_B_blank.py](#set_B_blank)
- [set_C_blank.py](#set_C_blank)
- [set_D_blank.py](#set_D_blank)
- [set_E_blank.py](#set_E_blank)
- [set_F_blank.py](#set_F_blank)
- [set_G_blank.py](#set_G_blank)
- [set_H_blank.py](#set_H_blank)
- [set_I_blank.py](#set_I_blank)
- [set_J_blank.py](#set_J_blank)
- [set_K_blank.py](#set_K_blank)
- [set_L_blank.py](#set_L_blank)
- [set_M_blank.py](#set_M_blank)
- [set_N_blank.py](#set_N_blank)
- [set_O_blank.py](#set_O_blank)
- [set_P_blank.py](#set_P_blank)
- [set_Q_blank.py](#set_Q_blank)
- [set_R_blank.py](#set_R_blank)
- [set_S_blank.py](#set_S_blank)
- [set_T_blank.py](#set_T_blank)
- [set_U_blank.py](#set_U_blank)
- [set_V_blank.py](#set_V_blank)
- [set_W_blank.py](#set_W_blank)
- [set_X_blank.py](#set_X_blank)
- [set_Y_blank.py](#set_Y_blank)
- [set_Z_blank.py](#set_Z_blank)

## set_AA_blank

端到端·并发版 AA（批量文件扫描→多线程解析→集中落库→汇总报表，含错误隔离与重试）- 空白版

要求：
- 扫描目录中的 *.csv 文件
- 使用 ThreadPoolExecutor 并发解析文件（解析：CSV→校验→转换 net/tax/period）
- 失败文件不影响整体（记录错误日志），针对临时错误支持有限重试
- 将所有成功记录集中写入 sqlite（单线程持久化）并输出汇总报表 CSV：period,dept,amount_sum,tax_sum
- 关键阶段输出 JSON 日志（scan_ok/parse_ok/parse_fail/persist_ok/report_ok）

```python
"""
端到端·并发版 AA（批量文件扫描→多线程解析→集中落库→汇总报表，含错误隔离与重试）- 空白版

要求：
- 扫描目录中的 *.csv 文件
- 使用 ThreadPoolExecutor 并发解析文件（解析：CSV→校验→转换 net/tax/period）
- 失败文件不影响整体（记录错误日志），针对临时错误支持有限重试
- 将所有成功记录集中写入 sqlite（单线程持久化）并输出汇总报表 CSV：period,dept,amount_sum,tax_sum
- 关键阶段输出 JSON 日志（scan_ok/parse_ok/parse_fail/persist_ok/report_ok）
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


# ===== 日志 =====
_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
_span_stack: contextvars.ContextVar[list[str]] = contextvars.ContextVar("span_stack", default=[])


class start_span:
    def __init__(self, name: str):
        self.name = name
        self._token_tid = None
        self._token_stk = None
        self._span_id = None

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


def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    # TODO：输出单行 JSON（至少包含 ts/level/msg/trace_id/span_id）
    pass


# ===== 读取与转换 =====
REQUIRED = ("code", "number", "amount", "rate", "date", "dept")
ALLOWED_RATES = {0.13, 0.09, 0.06, 0.03}
DATE_MIN = date(2000, 1, 1)
DATE_MAX = date(2100, 12, 31)


def validate_row(r: Dict[str, str]) -> Tuple[bool, str]:
    # TODO：检查必填与类型；新增业务校验：
    # - 金额非负；税率在集合 ALLOWED_RATES；日期在 [DATE_MIN, DATE_MAX]
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
    # TODO：进入 span，并解析 CSV → transform_rows
    return []


# ===== 持久化与报表 =====
def setup_db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute(
        "CREATE TABLE invoices( code TEXT, number TEXT, amount REAL, rate REAL, date TEXT, dept TEXT, net REAL, tax REAL, period TEXT, PRIMARY KEY(code,number))"
    )
    return con


def persist(con: sqlite3.Connection, rows: Iterable[Dict[str, Any]]) -> None:
    # TODO：参数化批量插入 OR REPLACE
    pass


def build_report(con: sqlite3.Connection) -> str:
    # TODO：SQL 汇总 + 写 CSV 文本
    return ""


def run_pipeline(root: str, logger: logging.Logger, max_workers: int = 4, retries: int = 1) -> str:
    # TODO：进入 root span；并发解析；失败重试一次；persist 与 report 加子 span
    files = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".csv")]
    log_json(logger, logging.INFO, "scan_ok", count=len(files))

    results: List[Dict[str, Any]] = []
    errors: List[str] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {}
        for p in files:
            futs[ex.submit(parse_file, p)] = (p, 0)
        for fut in as_completed(futs):
            p, _ = futs[fut]
            try:
                rows = fut.result()
                results.extend(rows)
                log_json(logger, logging.INFO, "parse_ok", file=os.path.basename(p), rows=len(rows))
            except Exception as e:
                log_json(logger, logging.ERROR, "parse_fail", file=os.path.basename(p), error=str(e))
                errors.append(os.path.basename(p))

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
        # 坏文件（缺列）
        with open(os.path.join(d, "bad.csv"), "w", encoding="utf-8") as f:
            f.write("oops")
        _make_csv(os.path.join(d, "b.csv"), [
            {"code": "002", "number": "002", "amount": 106, "rate": 0.06, "date": "2024-03-15", "dept": "A"},
        ])

        rep = run_pipeline(d, lg)
        lines = [ln for ln in rep.strip().splitlines() if ln.strip()]
        assert lines[0].startswith("period,dept,amount_sum,tax_sum")
        # 仅统计 a.csv 与 b.csv 的合计：219 与 19 税额（13+6）
        assert any(ln.startswith("2024-03,A,219.0,19.0") for ln in lines)

    print("[AA 空白版] 自检断言：全部通过（请完善 TODO 与实现）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_AB_blank

端到端·HTTP 服务版 AB（内置简易 HTTP API，接收 JSON 批次数据并返回报表）- 空白版

要求：
- 使用 http.server 实现 Handler：
  - POST /report：请求体为 {"rows": [...]}，每行包含 code,number,amount,rate,date,dept
  - 返回 JSON {"rows": [{"period":...,"dept":...,"amount_sum":...,"tax_sum":...}, ...]}
- 校验与转换同前（net/tax/period），出错返回 400 和错误信息
- 提供 /shutdown 关闭服务（仅测试使用）

```python
"""
端到端·HTTP 服务版 AB（内置简易 HTTP API，接收 JSON 批次数据并返回报表）- 空白版

要求：
- 使用 http.server 实现 Handler：
  - POST /report：请求体为 {"rows": [...]}，每行包含 code,number,amount,rate,date,dept
  - 返回 JSON {"rows": [{"period":...,"dept":...,"amount_sum":...,"tax_sum":...}, ...]}
- 校验与转换同前（net/tax/period），出错返回 400 和错误信息
- 提供 /shutdown 关闭服务（仅测试使用）
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
    # TODO：校验必填与类型；新增业务校验：
    # - 金额非负；税率属于 ALLOWED_RATES；日期在 [DATE_MIN, DATE_MAX]
    return True, ""


def aggregate(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # TODO：按 period,dept 汇总 amount 与 tax
    return []


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
                # TODO：校验与转换 rows（计算 period、net、tax），非法时返回 400
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
    # 启动服务
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    except Exception as e:
        print("[AB 空白版] 跳过：环境限制无法启动本地 HTTP 服务器。", e)
        return
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()

    # 构造请求
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
    # 应包含 2024-03/A 与 2024-04/B 两行
    got = {(r["period"], r["dept"]): (r["amount_sum"], r["tax_sum"]) for r in data["rows"]}
    assert got[("2024-03", "A")] == (219.0, 19.0) and got[("2024-04", "B")] == (113.0, 13.0)

    conn.request("POST", "/shutdown", body=b"{}", headers={"Content-Type": "application/json"})
    conn.getresponse().read()
    srv.server_close()
    print("[AB 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_A_blank

面试套题 A（基础与标准库）- 空白版

说明：
- 使用中文注释与命名，按提示在空白处（____）填写代码。
- 运行本文件将执行自检断言，全部通过即为正确。

涵盖：正则/字典推导/排序键/生成器/上下文管理器/CSV 读写

```python
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


```

## set_B_blank

面试套题 B（pandas 数据处理）- 空白版

说明：
- 需要 pandas（和可选 numpy）。建议用虚拟环境安装：pip install pandas numpy
- 本文件的自检中，涉及 Excel 的题使用了对 pandas.read_excel 的打桩以避免外部依赖。

```python
"""
面试套题 B（pandas 数据处理）- 空白版

说明：
- 需要 pandas（和可选 numpy）。建议用虚拟环境安装：pip install pandas numpy
- 本文件的自检中，涉及 Excel 的题使用了对 pandas.read_excel 的打桩以避免外部依赖。
"""

from __future__ import annotations

from typing import List


def read_merge_excel(path: str, sheets: List[str]):
    """读取多个 sheet 合并并重置索引。
    要求：pd.read_excel(path, sheet_name=..., dtype={____: str})
    """
    import pandas as pd

    dfs = [pd.read_excel(path, sheet_name=sh, dtype={____: str}) for sh in sheets]  # 填空
    out = pd.concat(dfs, ignore_index=True)
    return out.reset_index(drop=True)


def agg_by_dept(df):
    """对列 dept, amount, tax 分组聚合，amount 求和、tax 求均值，并按 amount_sum 降序"""
    g = df.groupby("dept").agg(amount_sum=("amount", "sum"), tax_avg=("tax", "mean"))
    return g.sort_values(by=____, ascending=False)  # 填空


def match_invoices(inv_df, org_df):
    """按 code, number 左连接，缺失部门填为 'UNK'"""
    m = inv_df.merge(org_df, on=["code", "number"], how=____)  # 填空
    m["dept"] = m["dept"].fillna("UNK")
    return m


def split_tax(df, rate: float):
    """向量化拆分：新增列 net(不含税) 与 tax(税额)，四舍五入两位"""
    import numpy as np

    amt = df["amount"].to_numpy(float)
    net = amt / (1 + rate)
    tax = amt - net
    df["net"] = np.round(____, 2)  # 填空：net
    df["tax"] = np.round(____, 2)  # 填空：tax
    return df


def add_period(df):
    """新增 period(月期) 与月末日期 month_end"""
    import pandas as pd

    df["period"] = df["date"].dt.to_period("M")
    df["month_end"] = df["date"] + pd.offsets.____(0)  # 填空：MonthEnd
    return df


def extract_taxno(df):
    """从 raw 列提取 15~20 位大写字母数字到 taxno，并将缺失填为 'NA'"""
    df["taxno"] = df["raw"].str.extract(r"([A-Z0-9]{15,20})", expand=False)
    df["taxno"] = df["taxno"].____("NA")  # 填空：fillna
    return df


def _run_self_tests():
    import pandas as pd

    # 1) 打桩 read_excel，避免外部引擎依赖
    calls = []

    def fake_read_excel(path, sheet_name, dtype):
        calls.append((path, sheet_name, dtype))
        return pd.DataFrame({"code": ["001"], "value": [sheet_name]})

    orig = pd.read_excel
    pd.read_excel = fake_read_excel  # type: ignore
    try:
        df = read_merge_excel("dummy.xlsx", ["S1", "S2"])
        assert list(df["value"]) == ["S1", "S2"]
        # 验证 dtype 传参中使用了某列名（空白处）
        assert isinstance(calls[0][2], dict) and len(calls[0][2]) == 1
    finally:
        pd.read_excel = orig  # type: ignore

    # 2)
    df = pd.DataFrame({"dept": ["A", "A", "B"], "amount": [1, 2, 5], "tax": [0.1, 0.2, 0.6]})
    g = agg_by_dept(df)
    assert list(g.index) == ["B", "A"] and float(g.loc["A", "amount_sum"]) == 3

    # 3)
    inv = pd.DataFrame({"code": ["c"], "number": ["n"], "amount": [100]})
    org = pd.DataFrame({"code": ["c"], "number": ["x"], "dept": ["D"]})
    m = match_invoices(inv, org)
    assert m.loc[0, "dept"] == "UNK"

    # 4)
    df2 = pd.DataFrame({"amount": [113.0]})
    df2 = split_tax(df2, 0.13)
    assert list(df2.columns) == ["amount", "net", "tax"] and round(df2.loc[0, "tax"], 2) == 13.0

    # 5)
    df3 = pd.DataFrame({"date": pd.to_datetime(["2024-03-15"])})
    df3 = add_period(df3)
    assert str(df3.loc[0, "period"]) == "2024-03" and str(df3.loc[0, "month_end"])[:10] == "2024-03-31"

    # 6)
    df4 = pd.DataFrame({"raw": ["税号 91350100M0001XU43T", "无"]})
    df4 = extract_taxno(df4)
    assert df4.loc[1, "taxno"] == "NA"

    print("[B 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_C_blank

面试套题 C（算法与 Pythonic）- 空白版

涵盖：LRU/堆/生成器/二分/itertools/dataclass 排序

```python
"""
面试套题 C（算法与 Pythonic）- 空白版

涵盖：LRU/堆/生成器/二分/itertools/dataclass 排序
"""

from __future__ import annotations

from collections import OrderedDict, Counter
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Tuple
import heapq
import itertools


@dataclass
class LRU:
    """基于 OrderedDict 的简易 LRU 缓存"""

    cap: int
    _d: OrderedDict = None

    def __post_init__(self):
        self._d = OrderedDict()

    def get(self, k):
        if k not in self._d:
            return -1
        v = self._d.pop(k)
        self._d[____] = v  # 填空：移动到尾部（最新）
        return v

    def put(self, k, v):
        if k in self._d:
            self._d.pop(k)
        elif len(self._d) >= self.cap:
            self._d.popitem(____)  # 填空：弹出最旧 last=False
        self._d[k] = v


def topk(words: List[str], k: int) -> List[Tuple[str, int]]:
    """返回出现频次前 k 的单词及其频次，频次降序、字典序升序"""
    cnt = Counter(words)
    heap: List[Tuple[int, str]] = []
    for w, c in cnt.items():
        heapq.heappush(heap, (____, w))  # 填空：(c, w)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(((w, c) for c, w in heap), key=lambda x: (-x[1], x[0]))


def flatten(xs: Iterable[Any]) -> Iterator[Any]:
    """扁平化嵌套的 list/tuple，其他类型原样输出"""
    for x in xs:
        if isinstance(x, (list, tuple)):
            ____ flatten(x)  # 填空：yield from
        else:
            yield x


def lower_bound(a: List[int], t: int) -> int:
    """返回第一个 >= t 的索引（上界）"""
    l, r = 0, len(a)
    while l < r:
        m = (l + r) // 2
        if a[m] < t:
            l = m + 1
        else:
            r = ____  # 填空：m
    return l


def rle(s: str):
    """运行长度编码，输出 (字符, 次数) 列表"""
    return [(ch, sum(1 for _ in grp)) for ch, grp in itertools.____(s)]  # 填空 groupby


@dataclass(order=True)
class Invoice:
    """用于排序的示例数据类：按 period 升序，再按 amount 降序"""

    period: str
    amount: float


def _run_self_tests():
    c = LRU(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1

    out = topk(list("aaabbc"), 2)
    assert out == [("a", 3), ("b", 2)]

    assert list(flatten([1, [2, (3, 4)], 5])) == [1, 2, 3, 4, 5]
    assert lower_bound([1, 2, 4, 4, 7], 4) == 2
    assert rle("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]

    rows = [Invoice("2024-03", 100), Invoice("2024-01", 200), Invoice("2024-03", 80)]
    out2 = sorted(rows, key=lambda x: (____, ____))  # 填空：x.period, -x.amount
    assert [r.amount for r in out2] == [200, 100, 80]

    print("[C 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_D_blank

面试套题 D（并发与性能）- 空白版

涵盖：线程池/asyncio/numpy/生成器分块/去重/日志

```python
"""
面试套题 D（并发与性能）- 空白版

涵盖：线程池/asyncio/numpy/生成器分块/去重/日志
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List
import asyncio
import logging


def process_all(xs: Iterable[int]) -> List[int]:
    """线程池并行执行 I/O 类任务，保持输入顺序"""

    def io_like(x: int) -> int:
        return x * x

    with ThreadPoolExecutor(max_workers=____) as ex:  # 填空：如 4
        return list(ex.map(io_like, xs))


async def fetch_one(x: int) -> int:
    await asyncio.sleep(0.01)
    return x + 1


async def gather_all(xs: List[int]) -> List[int]:
    """并发收集每个 fetch 的结果"""
    res = await asyncio.____(*(fetch_one(x) for x in xs))  # 填空：gather
    return list(res)


def split_vat_np(amounts, rate: float):
    """使用 numpy 向量化拆分含税金额。返回 (net, tax)。"""
    import numpy as np

    net = amounts / (1 + rate)
    tax = amounts - net
    return np.round(net, ____), np.round(tax, ____)  # 填空：2, 2


def read_chunks(lines: Iterable[str], n: int):
    """按 n 行分块生成，最后不足 n 的剩余块也会产出"""
    buf: List[str] = []
    for ln in lines:
        buf.append(ln)
        if len(buf) >= n:
            yield ____  # 填空：buf
            buf = []
    if buf:
        yield buf


def unique_keep_order(xs: Iterable[str]) -> List[str]:
    """去重但保持首次出现顺序"""
    seen = set()
    out: List[str] = []
    for x in xs:
        if x in seen:
            continue
        seen.add(____)  # 填空：x
        out.append(____)  # 填空：x
    return out


def setup_logger():
    """配置基础日志：INFO 级别，格式含时间/级别/消息"""
    logging.basicConfig(level=logging.____, format="____ - %(levelname)s - %(message)s")  # 填空：INFO, %(asctime)s
    return logging.getLogger("app")


def _run_self_tests():
    # 1) 线程池
    assert process_all([1, 2, 3]) == [1, 4, 9]

    # 2) asyncio
    out = asyncio.run(gather_all([1, 2, 3]))
    assert out == [2, 3, 4]

    # 3) numpy（若不可用则跳过）
    try:
        import numpy as np

        net, tax = split_vat_np(np.array([113.0]), 0.13)
        assert float(tax[0]) == 13.0
    except Exception as _:
        print("[D 空白版] 跳过 numpy 相关断言（未安装或环境不支持）")

    # 4) 分块
    chunks = list(read_chunks(["a", "b", "c", "d", "e"], 2))
    assert chunks == [["a", "b"], ["c", "d"], ["e"]]

    # 5) 去重保序
    assert unique_keep_order(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    # 6) 日志配置（不做严格断言，仅调用）
    lg = setup_logger()
    lg.info("日志配置完成")

    print("[D 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_E_blank

面试套题 E（业务综合）- 空白版

涵盖：个税/增值税/发票解析/脱敏/pandas 报表

```python
"""
面试套题 E（业务综合）- 空白版

涵盖：个税/增值税/发票解析/脱敏/pandas 报表
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import re


BRACKETS: List[Tuple[float, float, float]] = [
    (36000, 0.03, 0),
    (144000, 0.10, 2520),
    (300000, 0.20, 16920),
    (420000, 0.25, 31920),
    (660000, 0.30, 52920),
    (960000, 0.35, 85920),
    (float("inf"), 0.45, 181920),
]


def calc_iit(taxable: float) -> float:
    """根据简化税率表计算个税：税额=应纳税所得额*税率-速算扣除"""
    for top, rate, quick in BRACKETS:
        if taxable <= top:
            return round(____ * ____ - ____, 2)  # 填空：taxable, rate, quick
    return 0.0


def net_vat(invoices: List[Dict]) -> float:
    """销项税-进项税，金额为含税金额，税额=含税-不含税"""
    net = 0.0
    for inv in invoices:
        amt, r = float(inv["amount"]), float(inv["rate"])
        tax = amt - amt / (1 + r)
        if inv["type"] == "sale":
            net += tax
        else:
            net -= ____  # 填空：tax
    return round(net, 2)


def luhn_check(code: str) -> bool:
    s = 0
    alt = False
    for ch in reversed(code):
        if not ch.isdigit():
            return False
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        s += d
        alt = not alt
    return s % ____ == 0  # 填空：10


LINE_RE = re.compile(
    r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)"
)


def parse_line(s: str):
    m = LINE_RE.search(s)
    if not m:
        return None
    d = m.groupdict()
    d["amt"] = ____(d["amt"])  # 填空：float
    return d


def mask_account(s: str) -> str:
    """将连续 10~19 位数字的账号脱敏，保留末 4 位，其余用 * 替代"""
    return re.sub(r"(\d{6,15})(\d{4})", lambda m: "*" * len(m.group(1)) + m.group(2), s)


def monthly_report(df):
    """按月份与部门汇总金额并透视为列（需要 pandas）"""
    import pandas as pd

    df["period"] = df["date"].dt.to_period("M")
    g = df.groupby([____, ____])["amount"].sum().reset_index()  # 填空："period", "dept"
    p = g.pivot(index="period", columns="dept", values="amount").fillna(0)
    return p


def _run_self_tests():
    assert calc_iit(30000) == round(30000 * 0.03, 2)
    assert calc_iit(200000) == round(200000 * 0.20 - 16920, 2)

    invs = [{"type": "sale", "amount": 113, "rate": 0.13}, {"type": "purchase", "amount": 106, "rate": 0.06}]
    assert net_vat(invs) == round((113 - 100) - (106 - 100), 2)

    assert luhn_check("79927398713") is True

    x = parse_line("发票号:12345678 税号:91350100M0001XU43T 金额:113.00")
    assert x and x["no"] == "12345678" and isinstance(x["amt"], float)

    assert mask_account("账号 6222021234567890").endswith("7890")

    # pandas 测试（若不可用则跳过）
    try:
        import pandas as pd

        df = pd.DataFrame({
            "date": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-04-01"]),
            "dept": ["A", "B", "A"],
            "amount": [10, 20, 30],
        })
        rpt = monthly_report(df)
        assert str(rpt.index[0]) == "2024-03" and float(rpt.loc["2024-03", "A"]) == 10
    except Exception:
        print("[E 空白版] 跳过 pandas 相关断言（未安装或环境不支持）")

    print("[E 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_F_blank

面试套题 F（文本与高精度）- 空白版

涵盖：Decimal 高精度、正则多行解析、上下文管理、金额格式化、按键聚合、编码校验

```python
"""
面试套题 F（文本与高精度）- 空白版

涵盖：Decimal 高精度、正则多行解析、上下文管理、金额格式化、按键聚合、编码校验
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Dict, Iterable, Iterator, List, Tuple
import re


# 1) 使用 Decimal 高精度计算税额并四舍五入两位
def calc_tax_decimal(amount: str, rate: str) -> str:
    """输入为字符串形式的金额与税率，输出两位小数的税额字符串。例如：('113', '0.13') -> '13.00'"""
    a = Decimal(amount)
    r = Decimal(rate)
    tax = a * r / (Decimal(1) + r)
    with localcontext() as ctx:
        ctx.rounding = ____  # 填空：ROUND_HALF_UP
        return str(tax.quantize(Decimal("0.00")))


# 2) 正则多行解析发票文本，提取 no/taxno/amt
LINE_RE = re.compile(r"发票号:(?P<no>\d{8,12})\s+税号:(?P<taxno>[A-Z0-9]{15,20})\s+金额:(?P<amt>\d+(?:\.\d+)?)")


def parse_multilines(s: str) -> List[Dict[str, str]]:
    """从多行文本中解析多条发票信息"""
    out: List[Dict[str, str]] = []
    for m in LINE_RE.____(s):  # 填空：finditer
        out.append(m.groupdict())
    return out


# 3) 上下文管理：临时设置 Decimal 精度与舍入模式
class decimal_round:
    """示例上下文：进入时设置 rounding 与 prec，退出时恢复"""

    def __init__(self, rounding, prec: int):
        self.rounding = rounding
        self.prec = prec
        self._token = None

    def __enter__(self):
        self._ctx = localcontext()
        self._token = self._ctx.__enter__()
        self._ctx.rounding = ____  # 填空：self.rounding
        self._ctx.prec = ____      # 填空：self.prec
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._ctx.__exit__(exc_type, exc, tb)


# 4) 金额格式化（千分位，两位小数）
def fmt_amount(x: float) -> str:
    # 期望：1234567.8 -> '1,234,567.80'
    return f"{____:,.2f}"  # 填空：x


# 5) 按键聚合：合并相同 (code, number) 的金额求和
def merge_sum(rows: Iterable[Dict[str, float]]) -> List[Dict[str, float]]:
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["code"], r["number"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])  # 累加
    return [{"code": k[0], "number": k[1], "amount": v} for k, v in acc.items()]


# 6) 税号（大写字母数字 15~20 位）校验
def is_valid_taxno(s: str) -> bool:
    return re.fullmatch(r"[A-Z0-9]{15,20}", ____) is not None  # 填空：s


def _run_self_tests():
    # 1)
    assert calc_tax_decimal("113", "0.13") == "13.00"

    # 2)
    ms = parse_multilines("发票号:123 税号:INVALID 金额:1\n发票号:12345678 税号:91350100M0001XU43T 金额:113.00")
    assert ms[-1]["no"] == "12345678"

    # 3)
    with decimal_round(ROUND_HALF_UP, 10):
        # 精度与舍入设置不抛异常即可
        pass

    # 4)
    assert fmt_amount(1234567.8) == "1,234,567.80"

    # 5)
    rows = [
        {"code": "c1", "number": "n1", "amount": 10},
        {"code": "c1", "number": "n1", "amount": 2.5},
        {"code": "c2", "number": "n2", "amount": 3},
    ]
    out = merge_sum(rows)
    assert sorted(out, key=lambda x: x["code"]) == [
        {"code": "c1", "number": "n1", "amount": 12.5},
        {"code": "c2", "number": "n2", "amount": 3.0},
    ]

    # 6)
    assert is_valid_taxno("91350100M0001XU43T") is True
    assert is_valid_taxno("invalid") is False

    print("[F 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_G_blank

面试套题 G（pandas 进阶）- 空白版

涵盖：CSV 读取与类型、分类类型、环比/同比、滚动窗口、透视与合计、时区处理

```python
"""
面试套题 G（pandas 进阶）- 空白版

涵盖：CSV 读取与类型、分类类型、环比/同比、滚动窗口、透视与合计、时区处理
"""

from __future__ import annotations

from typing import List
import io


def read_csv_typed(csv_text: str):
    """读取 CSV 文本，解析日期列为 datetime64，code 列为 str。返回 DataFrame。"""
    import pandas as pd

    return pd.read_csv(io.StringIO(csv_text), parse_dates=[____], dtype={____: str})  # 填空：日期列名, code 列名


def to_categorical(df, col: str):
    """将指定列转换为分类类型"""
    df[col] = df[col].astype(____)  # 填空："category"
    return df


def add_mom_yoy(df, value_col: str):
    """按 period 列排序，增加环比 mom 与同比 yoy（以 12 期为周期）"""
    df = df.sort_values("period")
    df["mom"] = df[value_col].pct_change(____)  # 填空：1
    df["yoy"] = df[value_col].pct_change(____)  # 填空：12
    return df


def moving_avg(df, value_col: str, window: int = 3):
    """增加滚动窗口均值列 maN"""
    df[f"ma{window}"] = df[value_col].rolling(window, min_periods=1).mean()
    return df


def pivot_with_total(df):
    """按 period/dept 透视为列并添加行合计列 Total"""
    import pandas as pd

    p = df.pivot(index="period", columns="dept", values="amount").fillna(0)
    p["Total"] = ____  # 填空：按行求和 p.sum(axis=1)
    return p


def utc_to_shanghai(df, col: str):
    """将 UTC 时间列转换为上海时区（Asia/Shanghai）"""
    import pandas as pd

    s = df[col]
    s = s.dt.tz_localize("UTC").dt.tz_convert(____)  # 填空："Asia/Shanghai"
    df[col] = s
    return df


def _run_self_tests():
    try:
        import pandas as pd

        # 1) read_csv_typed
        text = "date,code,amount\n2024-01-01,001,10\n"
        d1 = read_csv_typed(text)
        assert str(d1.dtypes["date"]).startswith("datetime64") and str(d1.dtypes["code"]) == "object"

        # 2) to_categorical
        d2 = to_categorical(d1.copy(), "code")
        assert str(d2.dtypes["code"]) == "category"

        # 3) mom/yoy
        d3 = pd.DataFrame({
            "period": pd.period_range("2024-01", periods=13, freq="M"),
            "value": list(range(1, 14)),
        })
        d3 = add_mom_yoy(d3, "value")
        assert pd.isna(d3.loc[0, "mom"]) and pd.isna(d3.loc[0, "yoy"]) and round(d3.loc[12, "yoy"], 6) == 12/1 - 1

        # 4) moving avg
        d4 = moving_avg(pd.DataFrame({"v": [1, 2, 3]}), "v", 2)
        assert list(d4["ma2"]) == [1.0, 1.5, 2.5]

        # 5) pivot_with_total
        d5 = pd.DataFrame({
            "period": ["2024-03", "2024-03", "2024-04"],
            "dept": ["A", "B", "A"],
            "amount": [10, 20, 30],
        })
        p = pivot_with_total(d5)
        assert float(p.loc["2024-03", "Total"]) == 30

        # 6) 时区
        d6 = pd.DataFrame({"ts": pd.to_datetime(["2024-03-01T00:00:00Z"])})
        d6 = utc_to_shanghai(d6, "ts")
        assert str(d6.loc[0, "ts"].tz) == "Asia/Shanghai"

        print("[G 空白版] 自检断言：全部通过（请填写空白后再次验证）")
    except Exception as e:
        print("[G 空白版] 跳过：pandas 可能未安装。", e)


if __name__ == "__main__":
    _run_self_tests()


```

## set_H_blank

面试套题 H（并发进阶）- 空白版

涵盖：asyncio 并发限流、线程安全计数器、重试与退避、生产者-消费者

```python
"""
面试套题 H（并发进阶）- 空白版

涵盖：asyncio 并发限流、线程安全计数器、重试与退避、生产者-消费者
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, List
import threading
import time
import queue


# 1) asyncio 并发限流（信号量）
async def fetch_limited(xs: List[int], limit: int = 3) -> List[int]:
    sem = asyncio.Semaphore(limit)

    async def one(x: int) -> int:
        async with sem:
            await asyncio.sleep(0.01)
            return x * 2

    # 填空：并发收集
    res = await asyncio.____(*(one(x) for x in xs))  # 填空：gather
    return list(res)


# 2) 线程安全计数器（多线程累加）
class SafeCounter:
    def __init__(self) -> None:
        self._n = 0
        self._lock = threading.Lock()

    def inc(self, k: int = 1) -> None:
        # 填空：加锁更新
        with ____:  # 填空：self._lock
            self._n += k

    @property
    def value(self) -> int:
        return self._n


def add_with_threads(times: int = 1000, workers: int = 4) -> int:
    c = SafeCounter()
    def work():
        c.inc()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for _ in range(times):
            ex.submit(work)
    return c.value


# 3) 带重试的函数包装（指数退避）
def with_retry(fn: Callable[[], int], retries: int = 3) -> int:
    delay = 0.0
    for i in range(retries + 1):
        try:
            return fn()
        except Exception:
            if i == retries:
                raise
            # 填空：指数退避（无需实际等待太久）
            delay = ____ if delay == 0 else delay * 2  # 填空：0.01
            time.sleep(min(delay, 0.02))
    return 0


# 4) 生产者-消费者（有限队列）
def produce_consume(items: Iterable[int], maxsize: int = 8) -> List[int]:
    q: "queue.Queue[int]" = queue.Queue(maxsize=maxsize)
    out: List[int] = []
    stop = object()

    def producer():
        for x in items:
            q.put(x)
        q.put(stop)  # 结束标记

    def consumer():
        while True:
            v = q.get()
            if v is stop:
                break
            out.append(v * v)
            q.task_done()

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start(); t2.start()
    t1.join(); t2.join()
    return out


def _run_self_tests():
    # 1) asyncio 限流
    out = asyncio.run(fetch_limited(list(range(5)), limit=2))
    assert out == [0, 2, 4, 6, 8]

    # 2) 线程安全计数器
    assert add_with_threads(5000, 8) == 5000

    # 3) 重试
    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("fail")
        return 42
    assert with_retry(flaky, retries=5) == 42 and attempts["n"] == 3

    # 4) 生产者-消费者
    assert produce_consume([1, 2, 3]) == [1, 4, 9]

    print("[H 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_I_blank

面试套题 I（算法进阶）- 空白版

涵盖：Trie 敏感词脱敏、并查集、KMP、滑窗、快速选择、拓扑排序

```python
"""
面试套题 I（算法进阶）- 空白版

涵盖：Trie 敏感词脱敏、并查集、KMP、滑窗、快速选择、拓扑排序
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
from collections import deque, defaultdict


# 1) Trie 实现敏感词替换（将匹配的词用 * 替换，保持原长度）
class Trie:
    def __init__(self):
        self.next: Dict[str, Dict] = {}
        self.end = False

    def insert(self, word: str):
        node = self
        for ch in word:
            node = node.next.setdefault(ch, Trie())
        node.end = True

    def mask(self, s: str) -> str:
        n = len(s)
        res = list(s)
        for i in range(n):
            node = self
            j = i
            while j < n and s[j] in node.next:
                node = node.next[s[j]]
                j += 1
                if node.end:
                    # 覆盖 i..j-1 为 *
                    for k in range(i, j):
                        res[k] = '*'
        return ''.join(res)


# 2) 并查集（Union-Find）
class UnionFind:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1


# 3) KMP 查找子串首个位置；找不到返回 -1
def kmp_search(text: str, pat: str) -> int:
    if pat == "":
        return 0
    # 构建前缀函数
    pi = [0] * len(pat)
    j = 0
    for i in range(1, len(pat)):
        while j and pat[i] != pat[j]:
            j = pi[j - 1]
        if pat[i] == pat[j]:
            j += 1
        pi[i] = j
    # 匹配
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pat[j]:
            j = pi[j - 1]
        if ch == pat[j]:
            j += 1
            if j == len(pat):
                return i - j + 1
    return -1


# 4) 无重复字符的最长子串长度（滑动窗口）
def length_of_longest_substring(s: str) -> int:
    last = {}
    l = 0
    ans = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            l = last[ch] + 1
        last[ch] = r
        ans = max(ans, r - l + 1)
    return ans


# 5) 第 k 大元素（快速选择，k 从 1 开始）
def kth_largest(nums: List[int], k: int) -> int:
    import random
    target = len(nums) - k

    def select(lo: int, hi: int) -> int:
        if lo == hi:
            return nums[lo]
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        x = nums[hi]
        i = lo
        for j in range(lo, hi):
            if nums[j] <= x:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target:
            return nums[i]
        elif i < target:
            return select(i + 1, hi)
        else:
            return select(lo, i - 1)

    return select(0, len(nums) - 1)


# 6) 拓扑排序（Kahn 算法）。输入边列表，返回一种拓扑序；若有环返回空列表。
def topo_sort(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    indeg = [0] * n
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    out: List[int] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else []


def _run_self_tests():
    t = Trie(); [t.insert(w) for w in ["税务", "发票"]]
    assert t.mask("税务AI处理发票") == "**AI处理**"

    uf = UnionFind(5)
    uf.union(0, 1); uf.union(1, 2)
    assert uf.find(0) == uf.find(2) and uf.find(3) != uf.find(0)

    assert kmp_search("ababcababa", "ababa") == 5
    assert length_of_longest_substring("abcabcbb") == 3
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    order = topo_sort(4, [(0, 1), (1, 2), (0, 3)])
    assert order[:1] == [0] and set(order) == {0, 1, 2, 3}

    print("[I 空白版] 自检断言：全部通过（请根据题意在需要处填写空白再验证）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_J_blank

面试套题 J（业务进阶）- 空白版

涵盖：近似去重、JSON Lines 处理、税率分类、CSV 汇总导出、信用代码校验、舍入口径对比

```python
"""
面试套题 J（业务进阶）- 空白版

涵盖：近似去重、JSON Lines 处理、税率分类、CSV 汇总导出、信用代码校验、舍入口径对比
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import json
import io
import csv
import re


# 1) 发票近似去重（按 code, number 相同且金额差<=0.01 视为重复，保留第一条）
def dedupe_invoices(rows: Iterable[Dict]) -> List[Dict]:
    seen = {}
    out: List[Dict] = []
    for r in rows:
        key = (r["code"], r["number"])
        amt = float(r["amount"])
        if key not in seen or abs(seen[key] - amt) > 0.01:
            seen[key] = amt
            out.append(r)
    return out


# 2) 读取 JSON Lines，过滤 period=YYYY-MM 的记录
def read_filter_jsonl(text: str, period: str) -> List[Dict]:
    out: List[Dict] = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        if obj.get("period") == period:
            out.append(obj)
    return out


# 3) 根据税率分类标签
def rate_category(rate: float) -> str:
    # 例：0.13 -> "VAT13"，其他如 0.06 -> "VAT6"，未知 -> "OTHER"
    if rate in {0.13, 0.09, 0.06, 0.03}:  # 示例
        return f"VAT{int(rate*100)}"
    return "OTHER"


# 4) 汇总导出 CSV（按 period, dept 汇总 amount 求和并写出为 CSV 字符串）
def export_summary_csv(rows: Iterable[Dict]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["period", "dept", "amount"])
    # 填空：按 (period, dept) 聚合 amount 求和后写出
    acc: Dict[Tuple[str, str], float] = {}
    for r in rows:
        key = (r["period"], r["dept"])
        acc[key] = acc.get(key, 0.0) + float(r["amount"])
    for (p, d), v in sorted(acc.items()):
        writer.writerow([p, d, f"{v:.2f}"])
    return buf.getvalue()


# 5) 统一社会信用代码（简化校验：长度18且大写字母数字）
def is_valid_usci(code: str) -> bool:
    return re.fullmatch(r"[0-9A-Z]{18}", ____) is not None  # 填空：code


# 6) 舍入口径对比：银行家舍入 vs 四舍五入
def rounding_compare(x: str) -> Tuple[str, str]:
    d = Decimal(x)
    bank = d.quantize(Decimal("0.00"), rounding=____)       # 填空：ROUND_HALF_EVEN（银行家）
    halfup = d.quantize(Decimal("0.00"), rounding=____)     # 填空：ROUND_HALF_UP
    return (str(bank), str(halfup))


def _run_self_tests():
    # 1)
    rows = [
        {"code": "c", "number": "n", "amount": 100.00},
        {"code": "c", "number": "n", "amount": 100.005},  # 近似重复
        {"code": "c", "number": "n", "amount": 100.03},   # 超出阈值
    ]
    out = dedupe_invoices(rows)
    assert len(out) == 2

    # 2)
    text = "\n".join([
        json.dumps({"period": "2024-03", "v": 1}),
        json.dumps({"period": "2024-04", "v": 2}),
    ])
    got = read_filter_jsonl(text, "2024-03")
    assert len(got) == 1 and got[0]["v"] == 1

    # 3)
    assert rate_category(0.13) == "VAT13" and rate_category(0.07) == "OTHER"

    # 4)
    csv_text = export_summary_csv([
        {"period": "2024-03", "dept": "A", "amount": 10},
        {"period": "2024-03", "dept": "A", "amount": 2},
        {"period": "2024-03", "dept": "B", "amount": 5},
    ])
    assert "2024-03,A,12.00" in csv_text and "2024-03,B,5.00" in csv_text

    # 5)
    assert is_valid_usci("91350100M0001XU43T") is True
    assert is_valid_usci("91350100M0001XU43") is False
    assert is_valid_usci("91350100m0001XU43A") is False

    # 6)
    bank, up = rounding_compare("2.345")
    assert bank == "2.34" and up == "2.35"

    print("[J 空白版] 自检断言：全部通过（请填写空白后再次验证）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_K_blank

面试套题 K（混合题型-基础综合）- 空白版

题型包含：
- 选择题、判断题、编码实现、输出预测、小脚本实现

```python
"""
面试套题 K（混合题型-基础综合）- 空白版

题型包含：
- 选择题、判断题、编码实现、输出预测、小脚本实现
"""

from __future__ import annotations

from typing import Dict, List


# 选择题 Q1：关于列表与字典性能，下列说法正确的是？
# A. list 按值查找 O(1)
# B. dict 按键平均 O(1) 查找
# C. list append 平均 O(n)
# D. dict 遍历顺序随机（Py3.7+）
# 请将答案填写为 'A'/'B'/'C'/'D'
Q1_ANSWER = "___"  # 填你的选项


# 判断题 Q2：浅拷贝对嵌套可变对象只复制最外层容器引用（True/False）
Q2_ANSWER = None  # 填 True 或 False


# 编码题 Q3：手机号标准化
# - 移除非数字字符，仅保留最后 11 位（不足 11 位返回原数字串）
def normalize_phone(s: str) -> str:
    digits = [ch for ch in s if ch.isdigit()]
    num = "".join(digits)
    # TODO: 若长度>11，仅保留后 11 位
    return num  # 请修正


# 输出预测 Q4：请填写 PREDICT，与函数输出一致
def tricky(xs: List[int]) -> List[int]:
    xs2 = xs[:]
    ys = [i for i in range(3)]
    xs2.extend(ys)
    ys.append(99)
    return xs2

PREDICT = []  # 例如 [1,2,3]


# 小脚本 Q5：解析简易 INI 文本，支持 "key=value"，忽略空行与#注释
def parse_kv(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    # TODO：按行解析与 strip；'#' 开头或空行跳过
    for line in text.splitlines():
        pass
    return out


def _run_self_tests():
    # Q1
    assert Q1_ANSWER in {"A", "B", "C", "D"}
    assert Q1_ANSWER == "B"

    # Q2
    assert Q2_ANSWER is not None
    assert Q2_ANSWER is True

    # Q3
    assert normalize_phone("+86-138 0013 8000") == "13800138000"
    assert normalize_phone("12345") == "12345"

    # Q4
    assert PREDICT == tricky([7])

    # Q5
    txt = """
    # cfg
    a=1
    b = 2
    
    c=hello
    """.strip()
    got = parse_kv(txt)
    assert got == {"a": "1", "b": "2", "c": "hello"}

    print("[K 空白版] 自检断言：全部通过（请完善你的答案/实现后再运行）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_L_blank

面试套题 L（调试与修复）- 空白版

题型包含：修复 Bug、边界处理、日志配置与小型重构

```python
"""
面试套题 L（调试与修复）- 空白版

题型包含：修复 Bug、边界处理、日志配置与小型重构
"""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Tuple
import os


# 修复题 L1：字典合并
# 预期：返回 a 与 b 合并后的新字典（b 覆盖 a），且不修改原字典
def merge_dicts(a: Dict, b: Dict) -> Dict:
    c = a  # BUG：应创建副本
    c.update(b)  # OK：但此处会修改 a
    return c


# 修复题 L2：路径拼接（确保跨平台、避免多余分隔）
def join_path(root: str, *parts: str) -> str:
    # BUG：直接拼接
    return root + "/" + "/".join(parts)


# 修复题 L3：切分分块（每块最大 n，最后不足 n 也返回）
def chunk(xs: List[int], n: int) -> List[List[int]]:
    out = []
    i = 0
    while i < len(xs):
        out.append(xs[i : i + n])
        i += n
    return out


# 修复题 L4：日志配置（INFO 级别，格式包含时间/级别/消息）
def setup_logger(name: str = "app") -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")  # BUG：级别与格式不符合
    return logging.getLogger(name)


def _run_self_tests():
    # L1
    a = {"x": 1}; b = {"x": 2, "y": 3}
    c = merge_dicts(a, b)
    assert c == {"x": 2, "y": 3} and a == {"x": 1} and b == {"x": 2, "y": 3}

    # L2
    p = join_path("/root", "a", "b")
    assert p.endswith(os.path.join("a", "b")) and p.startswith("/root")

    # L3
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    # L4（不严格断言日志内容，仅调用）
    lg = setup_logger()
    lg.info("hello")

    print("[L 空白版] 自检断言：全部通过（修复上述函数以通过断言）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_M_blank

面试套题 M（设计与文档）- 空白版

题型包含：dataclass 设计、类型注解、聚合函数、选择题、文档说明生成

```python
"""
面试套题 M（设计与文档）- 空白版

题型包含：dataclass 设计、类型注解、聚合函数、选择题、文档说明生成
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Iterable, List


# 设计题 M1：实现交易数据类 Transaction
# 要求：
# - 字段：tid(str)、amount(Decimal)、currency(str)
# - 校验：amount >= 0；currency ∈ {"CNY","USD","EUR"}
# - 排序：按 currency 升序，再按 amount 降序
@dataclass(order=True)
class Transaction:
    # TODO：完善字段与 __post_init__ 校验与排序需要的字段顺序
    tid: str = ""
    amount: Decimal = Decimal("0")
    currency: str = "CNY"

    def __post_init__(self):
        pass


# 实现 M2：聚合同币种总额，返回 {currency: Decimal}
def aggregate_amounts(rows: Iterable[Transaction]) -> Dict[str, Decimal]:
    # TODO 实现
    return {}


# 选择题 M3：关于 typing.Protocol 与 ABC，哪项正确？
# A. Protocol 运行时检查实现
# B. Protocol 支持结构化子类型（鸭子类型）
# C. ABC 只能用于函数参数
# D. Protocol 不能定义属性
M3_ANSWER = "__"  # 选择一项


# 文档生成 M4：生成一段说明，至少包含“幂等”和“边界”两个关键词
def generate_doc() -> str:
    # TODO：返回包含关键词的简短说明
    return ""


def _run_self_tests():
    rows = [
        Transaction("t1", Decimal("10.00"), "CNY"),
        Transaction("t2", Decimal("5.00"), "USD"),
        Transaction("t3", Decimal("7.00"), "CNY"),
    ]

    # M1 排序
    out = sorted(rows, key=lambda x: (x.currency, -float(x.amount)))
    assert [x.tid for x in out] == ["t1", "t3", "t2"]

    # M2 聚合
    agg = aggregate_amounts(rows)
    assert agg == {"CNY": Decimal("17.00"), "USD": Decimal("5.00")}

    # M3
    assert M3_ANSWER in {"A", "B", "C", "D"}
    assert M3_ANSWER == "B"

    # M4
    doc = generate_doc()
    assert "幂等" in doc and "边界" in doc

    print("[M 空白版] 自检断言：全部通过（请完善实现与答案）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_N_blank

面试套题 N（异常与上下文）- 空白版

题型包含：上下文管理器、异常包装、重试装饰器、选择题

```python
"""
面试套题 N（异常与上下文）- 空白版

题型包含：上下文管理器、异常包装、重试装饰器、选择题
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable
import tempfile
import os
import time


# 上下文 N1：安全写文件，失败时仍确保关闭，且异常信息前缀为 "WRITE_FAIL:" 后再抛出
@contextmanager
def safe_write(path: str):
    f = None
    try:
        f = open(path, "w", encoding="utf-8")
        yield f
    except Exception as e:
        # TODO：包装异常并抛出
        raise
    finally:
        if f:
            f.close()


# 装饰器 N2：带最大尝试次数与固定间隔的重试
def retry(max_times: int = 3, delay: float = 0.01):
    def deco(fn: Callable):
        def wrapper(*args, **kwargs):
            # TODO：失败则重试，达到上限后抛出
            return fn(*args, **kwargs)
        return wrapper
    return deco


# 选择题 N3：关于 try/except/else/finally 哪项正确？
# A. else 在 except 执行后执行
# B. finally 仅在无异常时执行
# C. else 在 try 块不抛异常时执行
# D. except 会屏蔽 finally
N3_ANSWER = "__"


def _run_self_tests():
    # N1：成功写
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        with safe_write(tmp.name) as f:
            f.write("ok")
        with open(tmp.name, "r", encoding="utf-8") as fr:
            assert fr.read() == "ok"
    finally:
        os.unlink(tmp.name)

    # N1：失败时抛出带前缀
    try:
        with safe_write("/root/forbidden/path.txt") as f:
            f.write("x")
        raised = False
    except Exception as e:
        raised = True
        assert str(e).startswith("WRITE_FAIL:")
    assert raised

    # N2：重试
    calls = {"n": 0}

    @retry(max_times=3, delay=0.001)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return 42

    assert flaky() == 42 and calls["n"] == 3

    # N3
    assert N3_ANSWER in {"A", "B", "C", "D"}
    assert N3_ANSWER == "C"

    print("[N 空白版] 自检断言：全部通过（请完善实现与答案）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_O_blank

面试套题 O（算法与实战）- 空白版

题型包含：最短路（网格 BFS）、日志解析与统计、令牌化与清洗、JSON 结构变换

```python
"""
面试套题 O（算法与实战）- 空白版

题型包含：最短路（网格 BFS）、日志解析与统计、令牌化与清洗、JSON 结构变换
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Tuple
import json
import re


# O1：在 0/1 矩阵网格中从起点到终点的最短步数（4 邻接，1 表示障碍）
def shortest_path(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> int:
    # TODO：BFS 实现；无法到达返回 -1
    return -1


# O2：解析日志行，格式 "level=INFO ts=2024-01-01 msg=hello"，统计各 level 次数
def count_levels(lines: Iterable[str]) -> Dict[str, int]:
    # TODO：正则提取 level 值，大小写一致化
    return {}


# O3：令牌化文本，仅保留字母数字与中文，转小写，按空白切分
def tokenize(text: str) -> List[str]:
    # TODO：将非 [a-zA-Z0-9\u4e00-\u9fff\s] 替换为空格，再 split
    return []


# O4：将平铺 JSON 数组转为字典按某键分组
def group_by_key(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    out: Dict[str, List[Dict]] = {}
    for obj in items:
        k = str(obj.get(key, ""))
        out.setdefault(k, []).append(obj)
    return out


def _run_self_tests():
    # O1
    grid = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0],
    ]
    assert shortest_path(grid, (0, 0), (2, 2)) == 4

    # O2
    logs = [
        "level=info ts=... msg=hi",
        "level=INFO ts=... msg=ok",
        "level=warn ts=... msg=...",
    ]
    cnt = count_levels(logs)
    assert cnt == {"INFO": 2, "WARN": 1}

    # O3
    assert tokenize("Hello，世界! 100%") == ["hello", "世界", "100"]

    # O4
    items = [
        {"dept": "A", "v": 1},
        {"dept": "B", "v": 2},
        {"dept": "A", "v": 3},
    ]
    g = group_by_key(items, "dept")
    assert list(g.keys()) == ["A", "B"] and [x["v"] for x in g["A"]] == [1, 3]

    print("[O 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_P_blank

面试套题 P（日志与可观测性专项）- 空白版

题型：实现题 + 判断题
- JSON 结构化日志
- 上下文 request_id 注入
- 采样过滤器
- 耗时装饰器

```python
"""
面试套题 P（日志与可观测性专项）- 空白版

题型：实现题 + 判断题
- JSON 结构化日志
- 上下文 request_id 注入
- 采样过滤器
- 耗时装饰器
"""

from __future__ import annotations

import io
import json
import logging
import time
from typing import Any, Dict, Callable
import contextvars


# 上下文 request_id（用于注入到日志）
_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


def set_request_id(rid: str | None) -> None:
    _request_id.set(rid)


def get_request_id() -> str | None:
    return _request_id.get()


# P1：实现结构化日志输出为单行 JSON
def log_json(logger: logging.Logger, level: int, msg: str, **fields: Any) -> None:
    """输出一行 JSON，至少包含 ts/level/msg/request_id 字段，额外字段并入根层级。
    要求：
    - ts 使用 time.time() 的浮点秒
    - level 使用 logging.getLevelName(level) 的结果
    - request_id 从上下文变量读取（可为 None）
    """
    # TODO：实现
    pass


# P2：采样过滤器：每 N 条放行 1 条
class SamplingFilter(logging.Filter):
    def __init__(self, n: int = 10) -> None:
        super().__init__()
        self.n = n
        self._i = 0

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        # TODO：实现每 n 条放行一次
        return True


# P3：耗时装饰器：调用被装饰函数并记录 duration_ms 到日志
def measure_duration(logger: logging.Logger) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            # TODO：记录执行耗时并调用 log_json
            return fn(*args, **kwargs)
        return wrapper
    return deco


def _run_self_tests():
    # 准备 logger 与内存流
    stream = io.StringIO()
    logger = logging.getLogger("p_test")
    logger.handlers[:] = []
    h = logging.StreamHandler(stream)
    h.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

    # P1：基本 JSON 日志
    set_request_id("req-1")
    log_json(logger, logging.INFO, "hello", x=1)
    line = stream.getvalue().strip().splitlines()[-1]
    obj = json.loads(line)
    assert obj["msg"] == "hello" and obj["request_id"] == "req-1" and obj["x"] == 1 and "ts" in obj

    # P2：采样
    stream.seek(0); stream.truncate(0)
    # 清除采样过滤器，确保后续日志可见
    h.filters.clear()
    h.addFilter(SamplingFilter(3))
    for i in range(10):
        log_json(logger, logging.INFO, "s", i=i)
    lines = [ln for ln in stream.getvalue().splitlines() if ln.strip()]
    assert 3 <= len(lines) <= 4  # 10 条采样 1/3，应约 3~4 条

    # P3：耗时装饰器
    stream.seek(0); stream.truncate(0)
    h.filters.clear()

    @measure_duration(logger)
    def add(a, b):
        time.sleep(0.005)
        return a + b

    assert add(1, 2) == 3
    j = json.loads(stream.getvalue().splitlines()[-1])
    assert j["msg"] == "duration" and j["duration_ms"] >= 5

    print("[P 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

```

## set_Q_blank

面试套题 Q（数据脱敏与合规专项）- 空白版

题型：实现题
- 哈希+盐
- 姓名/邮箱脱敏
- k-匿名性检查
- 身份号正则检测（简化）

```python
"""
面试套题 Q（数据脱敏与合规专项）- 空白版

题型：实现题
- 哈希+盐
- 姓名/邮箱脱敏
- k-匿名性检查
- 身份号正则检测（简化）
"""

from __future__ import annotations

import hashlib
import re
from typing import Dict, Iterable, List


def hash_with_salt(text: str, salt: str) -> str:
    """返回 sha256(salt + text) 的 16 进制字符串"""
    # TODO：实现
    return ""


def mask_name(name: str) -> str:
    """中文姓名脱敏：保留首尾字符，中间用*号；长度<=2 时仅保留首字符"""
    # TODO：实现
    return name


def mask_email(email: str) -> str:
    """邮箱脱敏：姓名部分保留首字符，其他替换为 *，域名不变"""
    # 例如: alice@example.com -> a****@example.com
    # TODO：实现
    return email


def check_k_anonymity(rows: Iterable[Dict], quasi_keys: List[str], k: int) -> bool:
    """检查是否满足 k-匿名：每个 quasi_keys 分组的记录数 >= k"""
    # TODO：实现
    return True


def looks_like_cn_id(s: str) -> bool:
    """简化版中国身份证：18 位，前 17 位数字，最后一位为数字或大写 X"""
    # TODO：实现
    return False


def _run_self_tests():
    assert hash_with_salt("abc", "x") == hashlib.sha256(b"xabc").hexdigest()
    assert mask_name("张三丰") == "张*丰" and mask_name("李四") == "李*"
    assert mask_email("alice@example.com").startswith("a****@example.com")

    rows = [
        {"dept": "A", "city": "BJ", "age": 30},
        {"dept": "A", "city": "BJ", "age": 31},
        {"dept": "B", "city": "SH", "age": 29},
        {"dept": "B", "city": "SH", "age": 28},
    ]
    assert check_k_anonymity(rows, ["dept", "city"], 2) is True
    assert check_k_anonymity(rows, ["dept", "city"], 3) is False

    assert looks_like_cn_id("11010519491231002X") is True
    assert looks_like_cn_id("11010519491231002x") is False
    assert looks_like_cn_id("123") is False

    print("[Q 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_R_blank

面试套题 R（SQLite 与 SQL 安全）- 空白版

题型：实现题（仅标准库 sqlite3）
- 建表、主键、参数化插入
- 左连接汇总
- 防 SQL 注入（参数化）

```python
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


```

## set_S_blank

面试套题 S（API 设计与契约测试，纯标准库）- 空白版

题型：实现题
- 路由分发（方法+路径）
- 查询参数解析与校验
- JSON 请求体校验与业务处理
- 错误码与错误消息

```python
"""
面试套题 S（API 设计与契约测试，纯标准库）- 空白版

题型：实现题
- 路由分发（方法+路径）
- 查询参数解析与校验
- JSON 请求体校验与业务处理
- 错误码与错误消息
"""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple
from urllib.parse import parse_qs


def handle_request(method: str, path: str, query: str, body: str) -> Tuple[int, Dict[str, str], Dict[str, Any]]:
    """返回 (status, headers, body_json)；headers 至少含 {'Content-Type':'application/json'}
    路由：
    - GET /ping -> {"pong":true}
    - GET /add?a=1&b=2 -> {"sum":3}
    - POST /split_tax {"amount":113,"rate":0.13} -> {"net":100.0,"tax":13.0}
    错误：
    - 参数缺失/类型错误 -> 400
    - 未知路由 -> 404
    """
    headers = {"Content-Type": "application/json"}
    # TODO：实现
    return 500, headers, {"error": "not implemented"}


def _run_self_tests():
    st, hd, bj = handle_request("GET", "/ping", "", "")
    assert st == 200 and bj == {"pong": True}

    st, _, bj = handle_request("GET", "/add", "a=1&b=2", "")
    assert st == 200 and bj["sum"] == 3

    st, _, bj = handle_request("POST", "/split_tax", "", json.dumps({"amount": 113, "rate": 0.13}))
    assert st == 200 and round(bj["tax"], 2) == 13.0

    st, _, bj = handle_request("GET", "/add", "a=x&b=2", "")
    assert st == 400 and "error" in bj

    st, _, _ = handle_request("GET", "/nope", "", "")
    assert st == 404

    print("[S 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_T_blank

面试套题 T（异步任务编排专项）- 空白版

题型：实现题（asyncio）
- 任务去重（按 key）
- 队列与背压（最大队列长度）
- 重试与退避（带抖动）
- 优雅关闭

```python
"""
面试套题 T（异步任务编排专项）- 空白版

题型：实现题（asyncio）
- 任务去重（按 key）
- 队列与背压（最大队列长度）
- 重试与退避（带抖动）
- 优雅关闭
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Awaitable, Callable, Dict, Set


class TaskManager:
    def __init__(self, maxsize: int = 8, retries: int = 2) -> None:
        self.queue: "asyncio.Queue[tuple[str, Callable[[], Awaitable[Any]]]]" = asyncio.Queue(maxsize=maxsize)
        self.retries = retries
        self._keys_inflight: Set[str] = set()
        self._worker: asyncio.Task | None = None
        self._closed = False

    async def start(self) -> None:
        # TODO：启动后台 worker
        pass

    async def close(self) -> None:
        # TODO：优雅关闭：等待队列清空并取消 worker
        pass

    async def submit(self, key: str, coro_factory: Callable[[], Awaitable[Any]]) -> bool:
        """提交任务；若 key 已在队列或执行中，则返回 False（去重）"""
        # TODO：实现去重与队列放入
        return True

    async def _run(self):
        while True:
            key, fn = await self.queue.get()
            try:
                # TODO：带重试与指数退避（含抖动 0~10ms）
                pass
            finally:
                self._keys_inflight.discard(key)
                self.queue.task_done()


async def _run_self_tests():
    tm = TaskManager(maxsize=2, retries=2)
    await tm.start()

    seen: list[int] = []

    async def work(x: int):
        await asyncio.sleep(0.005)
        seen.append(x)
        return x

    # 去重：相同 key 只保留一次
    ok1 = await tm.submit("k1", lambda: work(1))
    ok2 = await tm.submit("k1", lambda: work(99))
    assert ok1 is True and ok2 is False

    # 背压：队列满时等待（这里不易精确断言，提交后关闭等待）
    await tm.submit("k2", lambda: work(2))
    await tm.submit("k3", lambda: work(3))

    # 重试：第一次失败后成功
    calls = {"n": 0}

    async def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("boom")
        return 42

    await tm.submit("k4", flaky)

    await tm.close()
    assert calls["n"] >= 2 and set(seen) >= {1, 2, 3}
    print("[T 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    asyncio.run(_run_self_tests())


```

## set_U_blank

专项套题 U（Tracing/可观测性-OpenTelemetry 风格模拟，纯标准库）- 空白版

目标：在不依赖第三方库的情况下，模拟 trace/span 上下文与事件日志。

包含：
- 上下文变量：trace_id、span 栈
- 上下文管理器：start_span(name)
- 事件输出：log_event(logger, name, **fields) -> 单行 JSON（含 trace/span）

```python
"""
专项套题 U（Tracing/可观测性-OpenTelemetry 风格模拟，纯标准库）- 空白版

目标：在不依赖第三方库的情况下，模拟 trace/span 上下文与事件日志。

包含：
- 上下文变量：trace_id、span 栈
- 上下文管理器：start_span(name)
- 事件输出：log_event(logger, name, **fields) -> 单行 JSON（含 trace/span）
"""

from __future__ import annotations

import contextvars
import io
import json
import logging
import time
import uuid
from typing import Any, Dict


_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
_span_stack: contextvars.ContextVar[list[str]] = contextvars.ContextVar("span_stack", default=[])


def current_ids() -> tuple[str | None, str | None]:
    stk = _span_stack.get()
    sid = stk[-1] if stk else None
    return _trace_id.get(), sid


class start_span:
    """进入新 span；若无 trace 则新建 trace_id。"""

    def __init__(self, name: str):
        self.name = name
        self._token_stk = None
        self._token_tid = None
        self._new_span = None

    def __enter__(self):
        tid = _trace_id.get()
        if tid is None:
            tid = ____  # 填空：uuid.uuid4().hex
            self._token_tid = _trace_id.set(tid)
        stk = list(_span_stack.get())
        self._new_span = ____  # 填空：uuid.uuid4().hex
        stk.append(self._new_span)
        self._token_stk = _span_stack.set(stk)
        return self

    def __exit__(self, exc_type, exc, tb):
        stk = list(_span_stack.get())
        if stk and stk[-1] == self._new_span:
            stk.pop()
        _span_stack.set(stk)
        if self._token_tid is not None:
            _trace_id.reset(self._token_tid)
        if self._token_stk is not None:
            _span_stack.reset(self._token_stk)
        return False


def log_event(logger: logging.Logger, name: str, **fields: Any) -> None:
    """输出单行 JSON，字段至少包含 ts, name, trace_id, span_id。"""
    # TODO：实现
    pass


def _run_self_tests():
    stream = io.StringIO()
    lg = logging.getLogger("u_test")
    lg.handlers[:] = []
    h = logging.StreamHandler(stream)
    h.setLevel(logging.INFO)
    lg.setLevel(logging.INFO)
    lg.addHandler(h)

    with start_span("root"):
        log_event(lg, "e1", x=1)
        with start_span("child"):
            log_event(lg, "e2", y=2)

    lines = [json.loads(ln) for ln in stream.getvalue().splitlines() if ln.strip()]
    assert len(lines) == 2
    assert lines[0]["name"] == "e1" and lines[1]["name"] == "e2"
    assert lines[0]["trace_id"] == lines[1]["trace_id"]
    assert lines[0]["span_id"] != lines[1]["span_id"]

    print("[U 空白版] 自检断言：全部通过（请完善填空）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_V_blank

专项套题 V（OCR 文本清洗与字段抽取，模拟）- 空白版

不依赖 OCR 库，给定“识别后文本”的字符串，完成：
- 规范化文本：标点/货币符号/常见误识别（O->0 等）
- 提取字段：发票代码 code、发票号码 number、金额 amount

```python
"""
专项套题 V（OCR 文本清洗与字段抽取，模拟）- 空白版

不依赖 OCR 库，给定“识别后文本”的字符串，完成：
- 规范化文本：标点/货币符号/常见误识别（O->0 等）
- 提取字段：发票代码 code、发票号码 number、金额 amount
"""

from __future__ import annotations

import re
from typing import Dict


def normalize_text(s: str) -> str:
    """规范化 OCR 文本：
    - 全角标点转半角：，：-> , :
    - 货币符号统一为 ¥
    - 常见误识别：字母 O 与 数字 0 的替换（仅在数字块内）
    - 统一标签：发票号/发票号码/票号 -> 发票号；纳税识别号/税号 -> 税号
    """
    # TODO：实现
    return s


LINE_RE = re.compile(r"发票号[:：]?(?P<number>\d{8,12}).*?代码[:：]?(?P<code>\d{10,12}).*?金额[:：]?(?P<amt>\d+(?:\.\d+)?)", re.S)


def extract_fields(s: str) -> Dict[str, str]:
    """从清洗后的文本中提取 code/number/amount"""
    m = LINE_RE.search(s)
    if not m:
        return {}
    d = m.groupdict()
    return {"code": d.get("code", ""), "number": d.get("number", ""), "amount": d.get("amt", "")}


def _run_self_tests():
    raw = """
    金额：RMB 113.OO
    票号: 12345678  税号: 91350100M0001XU43T
    代 码： 044031900111
    """.strip()
    s = normalize_text(raw)
    got = extract_fields(s)
    assert got["number"] == "12345678" and got["code"] == "044031900111" and got["amount"] in {"113.00", "113.0"}
    print("[V 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_W_blank

专项套题 W（批量数据导入流水线：校验→落库→回执）- 空白版

要求：
- validate_row(row) 校验必填字段：code, number, amount；类型正确
- import_rows(rows) 事务落库（sqlite3 内存库），返回汇总 {ok, fail, errors}

```python
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


```

## set_X_blank

专项套题 X（审计日志与轮转，纯标准库）- 空白版

要求：
- 写入事件为一行 JSON 文本
- 超过 max_bytes 后轮转：audit.log -> audit.log.1；保留 backups 个，超过则删除最旧

```python
"""
专项套题 X（审计日志与轮转，纯标准库）- 空白版

要求：
- 写入事件为一行 JSON 文本
- 超过 max_bytes 后轮转：audit.log -> audit.log.1；保留 backups 个，超过则删除最旧
"""

from __future__ import annotations

import json
import os
import tempfile
from typing import Any


class AuditLogger:
    def __init__(self, path: str, max_bytes: int = 128, backups: int = 2) -> None:
        self.path = path
        self.max_bytes = max_bytes
        self.backups = backups

    def _rotate(self) -> None:
        # TODO：从最大的序号开始往后移动，最后将当前文件改名为 .1
        pass

    def write(self, event: dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        line = json.dumps(event, ensure_ascii=False) + "\n"
        # TODO：若写入后超过 max_bytes，则先 rotate 再写
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)


def _run_self_tests():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "audit.log")
        lg = AuditLogger(p, max_bytes=50, backups=2)
        for i in range(20):
            lg.write({"i": i, "msg": "x" * 10})
        # 至少应有当前文件与 .1 存在
        assert os.path.exists(p) and os.path.exists(p + ".1")
    print("[X 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_Y_blank

专项套题 Y（简易规则引擎）- 空白版

规则格式（示例）：
[
  {"when": {"field": "amount", "op": "gt", "value": 100}, "then": {"set": {"flag": "HIGH"}}},
  {"when": {"field": "amount", "op": "gte", "value": 0}, "then": {"compute_tax": {"rate": 0.13}}}
]

要求：
- 支持条件操作符：eq/ne/gt/gte/lt/lte/in
- 支持动作：set（并入字段）、compute_tax（新增 tax=round(amount*rate/(1+rate),2)）

```python
"""
专项套题 Y（简易规则引擎）- 空白版

规则格式（示例）：
[
  {"when": {"field": "amount", "op": "gt", "value": 100}, "then": {"set": {"flag": "HIGH"}}},
  {"when": {"field": "amount", "op": "gte", "value": 0}, "then": {"compute_tax": {"rate": 0.13}}}
]

要求：
- 支持条件操作符：eq/ne/gt/gte/lt/lte/in
- 支持动作：set（并入字段）、compute_tax（新增 tax=round(amount*rate/(1+rate),2)）
"""

from __future__ import annotations

from typing import Any, Dict, List


def match(cond: Dict[str, Any], row: Dict[str, Any]) -> bool:
    # TODO：实现各操作符
    return False


def apply_actions(actions: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    # TODO：实现 set 与 compute_tax
    return row


def apply_rules(row: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    out = dict(row)
    for r in rules:
        if match(r.get("when", {}), out):
            out = apply_actions(r.get("then", {}), out)
    return out


def _run_self_tests():
    rules = [
        {"when": {"field": "amount", "op": "gt", "value": 100}, "then": {"set": {"flag": "HIGH"}}},
        {"when": {"field": "amount", "op": "gte", "value": 0}, "then": {"compute_tax": {"rate": 0.13}}},
    ]
    r = apply_rules({"amount": 113}, rules)
    assert r["flag"] == "HIGH" and round(r["tax"], 2) == 13.0
    print("[Y 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()


```

## set_Z_blank

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

```python
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


```
