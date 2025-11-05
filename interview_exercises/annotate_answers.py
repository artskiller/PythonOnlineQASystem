"""
为每套答案文件生成带注释的“注解版”文件 *_answers_annotated.py

规则：
- 读取对应的空白版，定位包含 "____" 的行，提取前后缀作为锚点；
- 在答案版中查找匹配行，插入中文注释，说明解题思路与答案来由；
- 不修改原始答案文件，输出注解版副本。

说明：
- 注释文本基于简单关键字启发式自动生成，覆盖正则/排序/并发/SQL/日志/日期/税额等常见考点。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent


EXPLAINS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"re\.compile\(.*\\d"), "使用正则非捕获组匹配整数/小数，便于统一提取数值"),
    (re.compile(r"datetime\.strptime|to_period|MonthEnd"), "日期标准化用于可比较/聚合，月末用 MonthEnd 偏移"),
    (re.compile(r"-r\[\"amount\"\]|-x\.amount"), "通过在排序键中取负数实现降序"),
    (re.compile(r"os\.chdir|contextmanager|__enter__|__exit__"), "上下文管理器确保进入/退出时资源恢复"),
    (re.compile(r"DictWriter|fieldnames|writerows"), "CSV 字段新增后统一写出，保持列顺序与表头"),
    (re.compile(r"MonthEnd"), "pandas 月末偏移量计算自然月末日期"),
    (re.compile(r"merge\(.*how=.*left"), "左连接保留左表记录，右侧缺失填默认值"),
    (re.compile(r"np\.round|round\(.*2\)"), "金额/税额统一四舍五入到两位"),
    (re.compile(r"OrderedDict.*popitem\(False\)"), "LRU 淘汰最旧元素（last=False）"),
    (re.compile(r"heapq\.heappush|heappop"), "小顶堆保留 TopK，键为(频次, 词) 实现稳定选择"),
    (re.compile(r"yield from"), "生成器委托递归扁平化嵌套结构"),
    (re.compile(r"while .* l < r|lower_bound"), "二分上界：满足条件时收缩右边界到 m"),
    (re.compile(r"itertools\.groupby"), "按相邻分组统计运行长度"),
    (re.compile(r"ThreadPoolExecutor|ex\.map"), "线程池并发处理 I/O，map 保持输入顺序"),
    (re.compile(r"asyncio\.gather|await.*sleep"), "协程并发收集任务结果"),
    (re.compile(r"logging\.basicConfig|%(asctime)s"), "结构化日志：包含时间/级别/消息，便于排查"),
    (re.compile(r"calc_iit|BRACKETS"), "个税速算：税额=应纳税所得额*税率-速算扣除"),
    (re.compile(r"s % 10 == 0|luhn"), "Luhn 校验：加权求和后对 10 取模"),
    (re.compile(r"re\.sub\(.*\*\*\*"), "正则分组替换：保留末尾，前段用 * 脱敏"),
    (re.compile(r"pivot\(|groupby\(|agg\("), "pandas 透视/聚合：按 period/dept 汇总"),
    (re.compile(r"contextvars|trace_id|span_id"), "注入 trace/span 上下文，形成可追踪链路日志"),
    (re.compile(r"sqlite3|executemany|\?\)"), "SQL 参数化避免注入，主键约束控制幂等"),
]


def explain_for_line(line: str) -> str:
    for pat, msg in EXPLAINS:
        if pat.search(line):
            return msg
    # 兜底：根据常见符号简单提示
    if "____" in line:
        return "依据函数语义补全占位，注意边界与类型一致性"
    if "= re." in line:
        return "正则优先使用预编译 pattern，提高复用与可读性"
    if "sorted(" in line and "key=" in line:
        return "自定义排序键，组合键体现业务优先级"
    return "按题目语义补全该处实现，保持风格一致"


def annotate_one(blank: Path, answer: Path) -> Path:
    b_lines = blank.read_text(encoding="utf-8").splitlines()
    a_lines = answer.read_text(encoding="utf-8").splitlines()

    # 收集占位锚点（前后缀）
    anchors: list[tuple[str, str]] = []
    for ln in b_lines:
        if "____" in ln:
            pre, _, post = ln.partition("____")
            # 去掉注释部分，避免与答案行不一致
            post = post.split('#', 1)[0]
            anchors.append((pre.strip(), post.strip()))

    # 在答案中逐个插入注释（避免重复）
    out: list[str] = []
    used = set()
    for i, ln in enumerate(a_lines):
        # 尝试为当前行找到匹配的锚点
        matched = False
        for idx, (pre, post) in enumerate(anchors):
            if idx in used:
                continue
            ok_pre = bool(pre and pre in ln)
            ok_post = bool(post and post in ln)
            if ok_pre and (not post or ok_post):
                msg = explain_for_line(ln)
                out.append(f"# 思路：{msg}")
                matched = True
                used.add(idx)
                break
        out.append(ln)
    # 写注解版
    target = answer.with_name(answer.stem + "_annotated.py")
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    return target


def main() -> None:
    blanks = sorted(ROOT.glob("set_*_blank.py"), key=lambda p: p.name)
    for b in blanks:
        ans = b.with_name(b.name.replace("_blank.py", "_answers.py"))
        if ans.exists():
            annotate_one(b, ans)


if __name__ == "__main__":
    main()
