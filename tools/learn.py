#!/usr/bin/env python3
"""
交互式学习工具

用法：
  python learn.py --level 01              # 学习第1阶段
  python learn.py --hint --question A1    # 获取提示
  python learn.py --debug --question A1   # 调试模式
  python learn.py --review                # 复习模式
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

# 学习阶段配置
STAGES = {
    "01": {
        "name": "基础入门",
        "sets": ["A", "K"],
        "dir": "exercises/01_basics",
        "description": "掌握 Python 核心语法和标准库",
    },
    "02": {
        "name": "数据处理",
        "sets": ["B", "G"],
        "dir": "exercises/02_data",
        "description": "掌握 pandas/numpy 数据分析技能",
    },
    "03": {
        "name": "算法思维",
        "sets": ["C", "I", "O"],
        "dir": "exercises/03_algorithm",
        "description": "提升算法设计和问题解决能力",
    },
    "04": {
        "name": "并发编程",
        "sets": ["D", "H", "T"],
        "dir": "exercises/04_concurrency",
        "description": "掌握多线程和异步编程",
    },
    "05": {
        "name": "工程实践",
        "sets": ["L", "N", "P", "M"],
        "dir": "exercises/05_engineering",
        "description": "掌握生产级代码的工程实践",
    },
    "06": {
        "name": "业务应用",
        "sets": ["E", "J", "F", "Q"],
        "dir": "exercises/06_business",
        "description": "将技术应用到实际业务场景",
    },
    "07": {
        "name": "系统设计",
        "sets": ["R", "S", "U", "V", "W", "X", "Y"],
        "dir": "exercises/07_system",
        "description": "设计和实现完整的系统组件",
    },
    "08": {
        "name": "综合项目",
        "sets": ["Z", "AA", "AB"],
        "dir": "exercises/08_projects",
        "description": "完成端到端的实战项目",
    },
}

# 提示系统（示例）
HINTS = {
    "A1": {
        1: "💡 提示1: 需要使用正则表达式匹配数字。整数是 \\d+，小数部分是可选的。",
        2: "💡 提示2: 可以使用 \\d+(\\.\\d+)? 来匹配整数或小数。",
        3: "💡 提示3: pattern = re.compile(r\"\\d+(?:\\.\\d+)?\")",
    },
    # 可以继续添加更多题目的提示
}


def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🎓 Python 交互式学习工具")
    print("=" * 60)
    print()


def list_stages():
    """列出所有学习阶段"""
    print("📚 学习阶段总览：\n")
    for stage_id, info in STAGES.items():
        sets_str = ", ".join(info["sets"])
        print(f"  {stage_id}. {info['name']}")
        print(f"      套题: {sets_str}")
        print(f"      说明: {info['description']}")
        print()


def learn_stage(stage_id: str):
    """学习指定阶段"""
    if stage_id not in STAGES:
        print(f"❌ 错误：阶段 {stage_id} 不存在")
        print("\n可用阶段：")
        list_stages()
        return 1

    stage = STAGES[stage_id]
    print(f"\n🎯 开始学习：第{stage_id}阶段 - {stage['name']}\n")
    print(f"📝 {stage['description']}\n")
    print(f"📂 目录：{stage['dir']}\n")
    print(f"📋 包含套题：{', '.join(stage['sets'])}\n")
    print("-" * 60)
    print("\n💡 学习建议：")
    print("  1. 进入目录：cd " + stage["dir"])
    print("  2. 查看题目：cat set_A_blank.py")
    print("  3. 编辑填空：vim set_A_blank.py")
    print("  4. 运行测试：python set_A_blank.py")
    print("  5. 对比答案：diff set_A_blank.py set_A_answers.py")
    print("  6. 查看注释：cat set_A_answers_annotated.py")
    print("\n📖 相关文档：")
    print("  - 学习路径：cat LEARNING_PATH.md")
    print("  - 知识图谱：cat KNOWLEDGE_MAP.md")
    print("  - 常见问题：cat FAQ.md")
    print()

    # 列出该阶段的所有文件
    stage_dir = Path(stage["dir"])
    if stage_dir.exists():
        print(f"\n📁 {stage['dir']} 目录下的文件：\n")
        for py_file in sorted(stage_dir.glob("*.py")):
            print(f"  - {py_file.name}")
    print()

    return 0


def show_hint(question: str, level: int = 1):
    """显示提示"""
    print(f"\n💡 题目 {question} 的提示（级别 {level}）：\n")

    if question not in HINTS:
        print(f"  暂无 {question} 的提示。")
        print(f"  建议：")
        print(f"    1. 查看题目要求和测试用例")
        print(f"    2. 查看 KNOWLEDGE_MAP.md 了解相关知识点")
        print(f"    3. 查看 set_{question[0]}_answers_annotated.py 的详细注释")
        return

    if level in HINTS[question]:
        print(f"  {HINTS[question][level]}")
    else:
        print(f"  没有级别 {level} 的提示。")
        print(f"  可用级别：{list(HINTS[question].keys())}")

    print()


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Python 交互式学习工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python learn.py --level 01              # 学习第1阶段
  python learn.py --hint --question A1    # 获取提示
  python learn.py --list                  # 列出所有阶段
        """,
    )

    parser.add_argument("--level", help="学习阶段（01-08）")
    parser.add_argument("--list", action="store_true", help="列出所有学习阶段")
    parser.add_argument("--hint", action="store_true", help="显示提示")
    parser.add_argument("--question", help="题目编号（如 A1）")
    parser.add_argument("--hint-level", type=int, default=1, help="提示级别（1-3）")
    parser.add_argument("--debug", action="store_true", help="调试模式（暂未实现）")
    parser.add_argument("--review", action="store_true", help="复习模式（暂未实现）")

    args = parser.parse_args(argv)

    print_banner()

    if args.list:
        list_stages()
        return 0

    if args.hint:
        if not args.question:
            print("❌ 错误：使用 --hint 时必须指定 --question")
            return 1
        show_hint(args.question, args.hint_level)
        return 0

    if args.level:
        return learn_stage(args.level)

    if args.debug:
        print("🔧 调试模式功能即将推出...")
        return 0

    if args.review:
        print("📖 复习模式功能即将推出...")
        return 0

    # 默认：显示帮助
    parser.print_help()
    print("\n💡 提示：使用 --list 查看所有学习阶段")
    return 0


if __name__ == "__main__":
    sys.exit(main())

