#!/usr/bin/env python3
"""
学习进度追踪工具

用法：
  python progress.py --show      # 显示学习进度
  python progress.py --week      # 本周进度
  python progress.py --stats     # 详细统计
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 学习阶段配置（与 learn.py 保持一致）
STAGES = {
    "01": {"name": "基础入门", "sets": ["A", "K"], "estimated_hours": 3.5},
    "02": {"name": "数据处理", "sets": ["B", "G"], "estimated_hours": 5.5},
    "03": {"name": "算法思维", "sets": ["C", "I", "O"], "estimated_hours": 9.0},
    "04": {"name": "并发编程", "sets": ["D", "H", "T"], "estimated_hours": 9.0},
    "05": {"name": "工程实践", "sets": ["L", "N", "P", "M"], "estimated_hours": 8.5},
    "06": {"name": "业务应用", "sets": ["E", "J", "F", "Q"], "estimated_hours": 11.0},
    "07": {"name": "系统设计", "sets": ["R", "S", "U", "V", "W", "X", "Y"], "estimated_hours": 17.5},
    "08": {"name": "综合项目", "sets": ["Z", "AA", "AB"], "estimated_hours": 14.0},
}

PROGRESS_FILE = Path(".learning_progress.json")


def load_progress() -> Dict:
    """加载学习进度"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "started": [], "last_update": None}


def save_progress(progress: Dict):
    """保存学习进度"""
    progress["last_update"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def check_file_completion(filepath: Path) -> bool:
    """检查文件是否完成（通过运行测试）"""
    if not filepath.exists():
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def scan_progress() -> Dict[str, Dict]:
    """扫描所有练习的完成情况"""
    progress = {}

    for stage_id, stage_info in STAGES.items():
        stage_progress = {
            "total": len(stage_info["sets"]),
            "completed": 0,
            "sets": {},
        }

        for set_name in stage_info["sets"]:
            # 检查空白版是否完成
            blank_file = Path(f"interview_exercises/set_{set_name}_blank.py")
            is_completed = check_file_completion(blank_file)

            stage_progress["sets"][set_name] = {
                "completed": is_completed,
                "file": str(blank_file),
            }

            if is_completed:
                stage_progress["completed"] += 1

        progress[stage_id] = stage_progress

    return progress


def show_progress():
    """显示学习进度"""
    print("=" * 70)
    print("📊 学习进度总览")
    print("=" * 70)
    print()

    progress = scan_progress()
    total_sets = sum(len(s["sets"]) for s in STAGES.values())
    total_completed = sum(p["completed"] for p in progress.values())
    total_hours = sum(s["estimated_hours"] for s in STAGES.values())

    # 计算已完成的预计时间
    completed_hours = 0
    for stage_id, stage_progress in progress.items():
        if stage_progress["completed"] > 0:
            stage_total = len(STAGES[stage_id]["sets"])
            stage_hours = STAGES[stage_id]["estimated_hours"]
            completed_hours += (stage_progress["completed"] / stage_total) * stage_hours

    # 显示各阶段进度
    for stage_id, stage_info in STAGES.items():
        stage_progress = progress[stage_id]
        completed = stage_progress["completed"]
        total = stage_progress["total"]
        percentage = (completed / total * 100) if total > 0 else 0

        # 状态图标
        if completed == 0:
            icon = "⬜"
        elif completed == total:
            icon = "✅"
        else:
            icon = "🔄"

        # 进度条
        bar_length = 20
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"{icon} 第{stage_id}阶段：{stage_info['name']}")
        print(f"   [{bar}] {completed}/{total} 题 ({percentage:.0f}%)")
        print(f"   预计时间：{stage_info['estimated_hours']:.1f} 小时")

        # 显示各套题状态
        if completed > 0 and completed < total:
            for set_name, set_info in stage_progress["sets"].items():
                status = "✓" if set_info["completed"] else "○"
                print(f"      {status} 套题 {set_name}")

        print()

    # 总体统计
    print("=" * 70)
    print(f"📈 总体进度：{total_completed}/{total_sets} 题 ({total_completed/total_sets*100:.1f}%)")
    print(f"⏱️  已用时间：约 {completed_hours:.1f} 小时")
    print(f"⏳ 预计剩余：约 {total_hours - completed_hours:.1f} 小时")
    print("=" * 70)
    print()

    # 学习建议
    if total_completed == 0:
        print("💡 建议：从第1阶段开始学习")
        print("   运行：python learn.py --level 01")
    elif total_completed < total_sets:
        # 找到下一个未完成的阶段
        for stage_id, stage_progress in progress.items():
            if stage_progress["completed"] < stage_progress["total"]:
                print(f"💡 建议：继续第{stage_id}阶段 - {STAGES[stage_id]['name']}")
                print(f"   运行：python learn.py --level {stage_id}")
                break
    else:
        print("🎉 恭喜！你已完成所有练习！")
        print("💡 建议：")
        print("   - 复习之前的题目")
        print("   - 尝试优化已完成的代码")
        print("   - 参与开源项目实践")

    print()


def show_stats():
    """显示详细统计"""
    print("=" * 70)
    print("📊 详细统计")
    print("=" * 70)
    print()

    progress = scan_progress()

    # 按难度统计
    easy = sum(1 for s in ["A", "K", "L", "M", "X", "F"] if any(
        p["sets"].get(s, {}).get("completed", False) for p in progress.values()
    ))
    medium = sum(1 for s in ["B", "C", "D", "N", "P", "R", "S"] if any(
        p["sets"].get(s, {}).get("completed", False) for p in progress.values()
    ))
    hard = sum(1 for s in ["E", "G", "H", "I", "J", "O", "Q", "T", "U", "V", "W", "Y"] if any(
        p["sets"].get(s, {}).get("completed", False) for p in progress.values()
    ))
    expert = sum(1 for s in ["Z", "AA", "AB"] if any(
        p["sets"].get(s, {}).get("completed", False) for p in progress.values()
    ))

    print("按难度分类：")
    print(f"  ⭐ 简单：{easy} 题")
    print(f"  ⭐⭐ 中等：{medium} 题")
    print(f"  ⭐⭐⭐ 困难：{hard} 题")
    print(f"  ⭐⭐⭐⭐ 专家：{expert} 题")
    print()

    # 按主题统计
    print("按主题分类：")
    themes = {
        "基础语法": ["A", "K"],
        "数据处理": ["B", "G"],
        "算法": ["C", "I", "O"],
        "并发": ["D", "H", "T"],
        "工程": ["L", "N", "P", "M"],
        "业务": ["E", "J", "F", "Q"],
        "系统": ["R", "S", "U", "V", "W", "X", "Y"],
        "项目": ["Z", "AA", "AB"],
    }

    for theme, sets in themes.items():
        completed = sum(1 for s in sets if any(
            p["sets"].get(s, {}).get("completed", False) for p in progress.values()
        ))
        print(f"  {theme}：{completed}/{len(sets)} 题")

    print()


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="学习进度追踪工具")
    parser.add_argument("--show", action="store_true", help="显示学习进度（默认）")
    parser.add_argument("--stats", action="store_true", help="显示详细统计")
    parser.add_argument("--week", action="store_true", help="本周进度（暂未实现）")

    args = parser.parse_args(argv)

    if args.stats:
        show_stats()
    elif args.week:
        print("📅 本周进度功能即将推出...")
    else:
        show_progress()

    return 0


if __name__ == "__main__":
    sys.exit(main())

