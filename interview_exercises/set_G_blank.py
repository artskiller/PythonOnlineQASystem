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

