"""
汇总生成脚本

功能：
- 汇总 interview_exercises 下所有套题为两份 Markdown：
  1) ALL_QUESTIONS.md（空白题版）
  2) ALL_SOLUTIONS.md（答案与解说版）

规则：
- 以文件名排序（set_A_* → set_B_* → ... → set_Z_* → set_AA_* ...）
- 每个文件输出：标题 + 可选说明（从文件开头三引号注释提取）+ 完整代码块
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Tuple

ROOT = Path(__file__).resolve().parent


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_docstring(text: str) -> str:
    m = re.match(r"\s*(?:\"\"\"|''')(.*?)(?:\"\"\"|''')", text, flags=re.S)
    return (m.group(1).strip() if m else "").strip()


def _collect(pattern: str) -> list[Path]:
    return sorted(ROOT.glob(pattern), key=lambda p: p.name)


KEYPOINTS = [
    (r"\bOrderedDict\b", "LRU 思路与有序字典应用（O(1) 更新/淘汰）"),
    (r"\bheapq\b", "小顶堆 TopK（O(n log k)）"),
    (r"\bitertools\b", "迭代工具（groupby/chain）"),
    (r"\byield from\b", "生成器委托与递归扁平化"),
    (r"\bdataclass\b", "数据类与排序键设计"),
    (r"\bpandas\b", "DataFrame 读写/聚合/向量化"),
    (r"\bnumpy\b", "数组向量化与广播"),
    (r"\basyncio\b", "协程并发（gather/信号量/队列）"),
    (r"ThreadPoolExecutor", "线程池（I/O 并发、保序 map）"),
    (r"@contextmanager|contextlib|__enter__\(|__exit__\(", "上下文管理器与资源安全释放"),
    (r"\blogging\b", "结构化日志与级别配置"),
    (r"\bsqlite3\b", "SQL 参数化、防注入、主键约束"),
    (r"\bhttp\.server\b|BaseHTTPRequestHandler", "标准库 HTTP 服务与路由分发"),
    (r"\bcontextvars\b|trace_id|span_id", "链路追踪（trace/span 上下文注入）"),
    (r"\bDecimal\b", "高精度小数与舍入模式"),
    (r"\bre\.compile|re\.search|re\.fullmatch\b", "正则提取/校验（边界/命名组/非捕获）"),
    (r"\bcsv\b", "CSV 读写、DictReader/Writer"),
    (r"\bjson\b", "JSON 解析与序列化（ensure_ascii/编码）"),
]

EDGEHINTS = [
    (r"round\(", "金额/税额舍入一致性（四舍五入两位）"),
    (r"pct_change\(", "环比/同比首行 NaN 处理"),
    (r"tz_localize|tz_convert", "时区与本地化转换"),
    (r"merge\(|join\(", "连接键类型一致与缺失填充"),
    (r"apply\(", "避免滥用 apply，优先向量化"),
    (r"executemany|\?\)", "SQL 参数化，避免拼接注入"),
    (r"Semaphore|Queue|gather", "并发限流/背压/异常聚合"),
    (r"os\.replace|rotate|backup", "日志轮转覆盖顺序与最旧清理"),
]


def _auto_explain(text: str) -> tuple[list[str], list[str]]:
    import re as _re
    points: list[str] = []
    edges: list[str] = []
    for pat, msg in KEYPOINTS:
        if _re.search(pat, text):
            points.append(msg)
    for pat, msg in EDGEHINTS:
        if _re.search(pat, text):
            edges.append(msg)
    # 去重并保持顺序
    def _dedup(xs: list[str]) -> list[str]:
        seen = set(); out = []
        for x in xs:
            if x in seen: continue
            seen.add(x); out.append(x)
        return out
    return _dedup(points), _dedup(edges)


def _build_markdown(files: Iterable[Path], title: str, with_explain: bool = False) -> str:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    # 目录索引
    lines.append("## 目录")
    for p in files:
        anchor = p.stem
        lines.append(f"- [{p.name}](#{anchor})")
    lines.append("")

    for p in files:
        text = _read(p)
        doc = _extract_docstring(text)
        lines.append(f"## {p.stem}")
        lines.append("")
        if doc:
            lines.append(doc)
            lines.append("")
        if with_explain:
            pts, eds = _auto_explain(text)
            if pts:
                lines.append("### 解题要点（自动提炼）")
                for s in pts:
                    lines.append(f"- {s}")
                lines.append("")
            if eds:
                lines.append("### 易错点/边界（自动提示）")
                for s in eds:
                    lines.append(f"- {s}")
                lines.append("")
        lines.append("```python")
        lines.append(text)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    blanks = _collect("set_*_blank.py")
    answers = _collect("set_*_answers.py")

    q_md = _build_markdown(blanks, "面试套题汇总（空白题）", with_explain=False)
    a_md = _build_markdown(answers, "面试套题汇总（答案与解说）", with_explain=True)

    (ROOT / "ALL_QUESTIONS.md").write_text(q_md, encoding="utf-8")
    (ROOT / "ALL_SOLUTIONS.md").write_text(a_md, encoding="utf-8")


if __name__ == "__main__":
    main()
