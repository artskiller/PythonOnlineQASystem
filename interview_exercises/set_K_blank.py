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

