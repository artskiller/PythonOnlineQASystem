"""
面试套题 B（pandas 数据处理）- 答案版
"""

from __future__ import annotations

from typing import List


def read_merge_excel(path: str, sheets: List[str]):
    import pandas as pd

# 思路：按题目语义补全该处实现，保持风格一致
    dfs = [pd.read_excel(path, sheet_name=sh, dtype={"code": str}) for sh in sheets]
    out = pd.concat(dfs, ignore_index=True)
    return out.reset_index(drop=True)


def agg_by_dept(df):
    g = df.groupby("dept").agg(amount_sum=("amount", "sum"), tax_avg=("tax", "mean"))
# 思路：按题目语义补全该处实现，保持风格一致
    return g.sort_values(by="amount_sum", ascending=False)


def match_invoices(inv_df, org_df):
# 思路：左连接保留左表记录，右侧缺失填默认值
    m = inv_df.merge(org_df, on=["code", "number"], how="left")
    m["dept"] = m["dept"].fillna("UNK")
    return m


def split_tax(df, rate: float):
    import numpy as np

    amt = df["amount"].to_numpy(float)
    net = amt / (1 + rate)
    tax = amt - net
# 思路：金额/税额统一四舍五入到两位
    df["net"] = np.round(net, 2)
# 思路：金额/税额统一四舍五入到两位
    df["tax"] = np.round(tax, 2)
    return df


def add_period(df):
    import pandas as pd

    df["period"] = df["date"].dt.to_period("M")
# 思路：日期标准化用于可比较/聚合，月末用 MonthEnd 偏移
    df["month_end"] = df["date"] + pd.offsets.MonthEnd(0)
    return df


def extract_taxno(df):
    df["taxno"] = df["raw"].str.extract(r"([A-Z0-9]{15,20})", expand=False)
# 思路：按题目语义补全该处实现，保持风格一致
    df["taxno"] = df["taxno"].fillna("NA")
    return df


def _run_self_tests():
    import pandas as pd

    # 1) 打桩 read_excel
    calls = []

    def fake_read_excel(path, sheet_name, dtype):
        calls.append((path, sheet_name, dtype))
        return pd.DataFrame({"code": ["001"], "value": [sheet_name]})

    orig = pd.read_excel
    pd.read_excel = fake_read_excel  # type: ignore
    try:
        df = read_merge_excel("dummy.xlsx", ["S1", "S2"])
        assert list(df["value"]) == ["S1", "S2"]
        assert calls[0][2] == {"code": str}
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

    print("[B 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

