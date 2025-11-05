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

