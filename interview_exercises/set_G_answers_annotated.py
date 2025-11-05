"""
面试套题 G（pandas 进阶）- 答案版
"""

from __future__ import annotations

from typing import List
import io


def read_csv_typed(csv_text: str):
    import pandas as pd

    return pd.read_csv(io.StringIO(csv_text), parse_dates=["date"], dtype={"code": str})


def to_categorical(df, col: str):
# 思路：按题目语义补全该处实现，保持风格一致
    df[col] = df[col].astype("category")
    return df


def add_mom_yoy(df, value_col: str):
    df = df.sort_values("period")
# 思路：按题目语义补全该处实现，保持风格一致
    df["mom"] = df[value_col].pct_change(1)
# 思路：按题目语义补全该处实现，保持风格一致
    df["yoy"] = df[value_col].pct_change(12)
    return df


def moving_avg(df, value_col: str, window: int = 3):
    df[f"ma{window}"] = df[value_col].rolling(window, min_periods=1).mean()
    return df


def pivot_with_total(df):
    import pandas as pd

    p = df.pivot(index="period", columns="dept", values="amount").fillna(0)
# 思路：按题目语义补全该处实现，保持风格一致
    p["Total"] = p.sum(axis=1)
    return p


def utc_to_shanghai(df, col: str):
    import pandas as pd

    s = df[col]
# 思路：按题目语义补全该处实现，保持风格一致
    s = s.dt.tz_localize("UTC").dt.tz_convert("Asia/Shanghai")
    df[col] = s
    return df


def _run_self_tests():
    try:
        import pandas as pd
        text = "date,code,amount\n2024-01-01,001,10\n"
        d1 = read_csv_typed(text)
        assert str(d1.dtypes["date"]).startswith("datetime64") and str(d1.dtypes["code"]) == "object"

        d2 = to_categorical(d1.copy(), "code")
        assert str(d2.dtypes["code"]) == "category"

        d3 = pd.DataFrame({
            "period": pd.period_range("2024-01", periods=13, freq="M"),
            "value": list(range(1, 14)),
        })
        d3 = add_mom_yoy(d3, "value")
        assert pd.isna(d3.loc[0, "mom"]) and pd.isna(d3.loc[0, "yoy"]) and round(d3.loc[12, "yoy"], 6) == 12/1 - 1

        d4 = moving_avg(pd.DataFrame({"v": [1, 2, 3]}), "v", 2)
        assert list(d4["ma2"]) == [1.0, 1.5, 2.5]

        d5 = pd.DataFrame({
            "period": ["2024-03", "2024-03", "2024-04"],
            "dept": ["A", "B", "A"],
            "amount": [10, 20, 30],
        })
        p = pivot_with_total(d5)
        assert float(p.loc["2024-03", "Total"]) == 30

        d6 = pd.DataFrame({"ts": pd.to_datetime(["2024-03-01T00:00:00Z"])})
        d6 = utc_to_shanghai(d6, "ts")
        assert str(d6.loc[0, "ts"].tz) == "Asia/Shanghai"

        print("[G 答案版] 自检断言：全部通过")
    except Exception as e:
        print("[G 答案版] 跳过：pandas 可能未安装。", e)


if __name__ == "__main__":
    _run_self_tests()

