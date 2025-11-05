#!/usr/bin/env python3
"""
面试模拟器 - 2小时限时练习

用法：
  python interview_simulator.py --duration 120 --focus tax    # 侧重财税
  python interview_simulator.py --duration 120 --difficulty medium
  python interview_simulator.py --random 10                   # 随机10题
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# 题目分类配置
QUESTION_SETS = {
    # 财税业务（重点）
    "tax": {
        "sets": ["E", "J", "F", "Q"],
        "description": "财税业务（个税/增值税/发票/合规）",
        "weight": 3,  # 权重
    },
    # AI技能（新增）
    "ai": {
        "sets": ["ML1", "NLP1", "OCR1"],
        "description": "AI技能（机器学习/NLP/OCR）",
        "weight": 3,
    },
    "ml": {
        "sets": ["ML1"],
        "description": "机器学习基础",
        "weight": 1,
    },
    "nlp": {
        "sets": ["NLP1"],
        "description": "自然语言处理",
        "weight": 1,
    },
    "ocr": {
        "sets": ["OCR1"],
        "description": "OCR图像识别",
        "weight": 1,
    },
    # 数据处理
    "data": {
        "sets": ["B", "G"],
        "description": "数据处理（pandas/numpy）",
        "weight": 2,
    },
    # 并发编程
    "concurrency": {
        "sets": ["D", "H", "T"],
        "description": "并发编程（asyncio/threading）",
        "weight": 2,
    },
    # 系统设计
    "system": {
        "sets": ["R", "S", "U", "V", "W", "X", "Y"],
        "description": "系统设计（API/日志/追踪）",
        "weight": 1,
    },
    # 基础
    "basics": {
        "sets": ["A", "K", "L", "M", "N", "P"],
        "description": "Python基础与工程实践",
        "weight": 1,
    },
    # 算法
    "algorithm": {
        "sets": ["C", "I", "O"],
        "description": "算法与数据结构",
        "weight": 1,
    },
    # 项目
    "project": {
        "sets": ["Z", "AA", "AB"],
        "description": "端到端项目",
        "weight": 1,
    },
}

# 难度配置
DIFFICULTY_SETS = {
    "easy": ["A", "K", "L", "M", "X", "F"],
    "medium": ["B", "C", "D", "N", "P", "R", "S", "E"],
    "hard": ["G", "H", "I", "J", "O", "Q", "T", "U", "V", "W", "Y"],
    "expert": ["Z", "AA", "AB"],
}


def select_questions(
    focus: str | None = None,
    difficulty: str | None = None,
    count: int | None = None,
    random_seed: int | None = None,
) -> List[str]:
    """选择题目"""
    if random_seed is not None:
        random.seed(random_seed)

    selected = []

    if focus:
        # 按主题选择
        if focus in QUESTION_SETS:
            sets = QUESTION_SETS[focus]["sets"]
            selected = sets if count is None else random.sample(sets, min(count, len(sets)))
        else:
            print(f"⚠️  未知主题: {focus}")
            print(f"可用主题: {', '.join(QUESTION_SETS.keys())}")
            sys.exit(1)
    elif difficulty:
        # 按难度选择
        if difficulty in DIFFICULTY_SETS:
            sets = DIFFICULTY_SETS[difficulty]
            selected = sets if count is None else random.sample(sets, min(count, len(sets)))
        else:
            print(f"⚠️  未知难度: {difficulty}")
            print(f"可用难度: {', '.join(DIFFICULTY_SETS.keys())}")
            sys.exit(1)
    elif count:
        # 随机选择
        all_sets = list(set(s for cat in QUESTION_SETS.values() for s in cat["sets"]))
        selected = random.sample(all_sets, min(count, len(all_sets)))
    else:
        # 默认：财税为主的混合
        selected = []
        # 财税题目（50%）
        tax_sets = QUESTION_SETS["tax"]["sets"]
        selected.extend(random.sample(tax_sets, min(2, len(tax_sets))))
        # 数据处理（25%）
        data_sets = QUESTION_SETS["data"]["sets"]
        selected.extend(random.sample(data_sets, 1))
        # 其他（25%）
        other_sets = QUESTION_SETS["concurrency"]["sets"] + QUESTION_SETS["basics"]["sets"]
        selected.extend(random.sample(other_sets, 2))

    return sorted(selected)


def run_interview(
    questions: List[str],
    duration_minutes: int,
    output_dir: Path,
) -> Dict:
    """运行面试模拟"""
    print("=" * 70)
    print("🎯 面试模拟器")
    print("=" * 70)
    print()
    print(f"📋 题目数量: {len(questions)}")
    print(f"⏱️  限时: {duration_minutes} 分钟")
    print(f"📝 题目列表: {', '.join(questions)}")
    print()
    print("=" * 70)
    print()

    # 创建工作目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = output_dir / f"interview_{timestamp}"
    work_dir.mkdir(parents=True, exist_ok=True)

    # 复制题目到工作目录
    print("📁 准备题目文件...")
    for q in questions:
        src = Path(f"interview_exercises/set_{q}_blank.py")
        if src.exists():
            dst = work_dir / f"set_{q}_blank.py"
            dst.write_text(src.read_text())
            print(f"  ✓ {dst.name}")

    print()
    print("=" * 70)
    print("⏰ 面试开始！")
    print("=" * 70)
    print()
    print(f"📂 工作目录: {work_dir}")
    print()
    print("💡 提示:")
    print("  1. 在工作目录中编辑题目文件")
    print("  2. 运行 python set_X_blank.py 测试")
    print("  3. 时间到后会自动评分")
    print()

    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    print(f"⏱️  结束时间: {end_time.strftime('%H:%M:%S')}")
    print()
    print("按 Enter 开始计时...")
    input()

    start_time = time.time()
    print()
    print("⏰ 计时开始！")
    print()

    # 等待时间结束或用户提前结束
    try:
        print("💡 完成后按 Ctrl+C 提前结束，或等待时间到...")
        time.sleep(duration_minutes * 60)
        print("\n⏰ 时间到！")
    except KeyboardInterrupt:
        print("\n\n⏸️  提前结束")

    elapsed = time.time() - start_time
    print()
    print("=" * 70)
    print("📊 开始评分...")
    print("=" * 70)
    print()

    # 评分
    results = {}
    passed = 0
    failed = 0

    for q in questions:
        test_file = work_dir / f"set_{q}_blank.py"
        if not test_file.exists():
            results[q] = {"status": "missing", "output": "文件不存在"}
            failed += 1
            continue

        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                timeout=10,
                cwd=work_dir,
            )
            if result.returncode == 0:
                results[q] = {"status": "passed", "output": result.stdout.decode()}
                passed += 1
                print(f"✅ Set {q}: 通过")
            else:
                results[q] = {
                    "status": "failed",
                    "output": result.stdout.decode() + result.stderr.decode(),
                }
                failed += 1
                print(f"❌ Set {q}: 失败")
        except subprocess.TimeoutExpired:
            results[q] = {"status": "timeout", "output": "超时"}
            failed += 1
            print(f"⏱️  Set {q}: 超时")
        except Exception as e:
            results[q] = {"status": "error", "output": str(e)}
            failed += 1
            print(f"❌ Set {q}: 错误 - {e}")

    # 生成报告
    report = {
        "timestamp": timestamp,
        "duration_minutes": duration_minutes,
        "elapsed_seconds": int(elapsed),
        "questions": questions,
        "total": len(questions),
        "passed": passed,
        "failed": failed,
        "score": round(passed / len(questions) * 100, 1) if questions else 0,
        "results": results,
    }

    report_file = work_dir / "report.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print()
    print("=" * 70)
    print("📊 面试结果")
    print("=" * 70)
    print()
    print(f"⏱️  用时: {int(elapsed // 60)} 分 {int(elapsed % 60)} 秒")
    print(f"✅ 通过: {passed}/{len(questions)}")
    print(f"❌ 失败: {failed}/{len(questions)}")
    print(f"📈 得分: {report['score']}%")
    print()
    print(f"📄 详细报告: {report_file}")
    print()

    return report


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="面试模拟器")
    parser.add_argument("--duration", type=int, default=120, help="时长（分钟），默认120")
    parser.add_argument("--focus", choices=list(QUESTION_SETS.keys()), help="主题侧重")
    parser.add_argument("--difficulty", choices=list(DIFFICULTY_SETS.keys()), help="难度")
    parser.add_argument("--random", type=int, metavar="N", help="随机选择N题")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--output", type=Path, default=Path("interview_results"), help="输出目录")

    args = parser.parse_args(argv)

    # 选择题目
    questions = select_questions(
        focus=args.focus,
        difficulty=args.difficulty,
        count=args.random,
        random_seed=args.seed,
    )

    if not questions:
        print("❌ 没有选择任何题目")
        return 1

    # 运行面试
    report = run_interview(questions, args.duration, args.output)

    # 返回码：通过率 >= 60% 为成功
    return 0 if report["score"] >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())

