"""
一键运行所有自检脚本

用法：
  python interview_exercises/run_all.py --mode answers   # 默认，运行答案版
  python interview_exercises/run_all.py --mode blank     # 运行空白版（未填写将失败）
  python interview_exercises/run_all.py --mode both      # 先空白后答案

说明：
- B/E 套题依赖 pandas（可选 numpy），若未安装将自动跳过。
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parent


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def run_file(pyfile: Path) -> tuple[bool, str]:
    """运行单个 Python 文件，返回 (是否成功, 输出文本)。"""
    proc = subprocess.run([sys.executable, str(pyfile)], capture_output=True, text=True)
    ok = proc.returncode == 0
    out = (proc.stdout or "") + (proc.stderr or "")
    return ok, out


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="批量运行面试题自检")
    ap.add_argument("--mode", choices=["answers", "blank", "both"], default="answers")
    args = ap.parse_args(argv)

    sets = [
        "A","B","C","D","E","F","G","H","I","J",
        "K","L","M","N","O","P","Q","R","S","T",
        "U","V","W","X","Y","Z","AA","AB"
    ]
    want_blank = args.mode in ("blank", "both")
    want_answers = args.mode in ("answers", "both")

    pandas_ok = has_module("pandas")

    total = 0
    passed = 0
    skipped = 0

    def maybe_run(tag: str, kind: str):
        nonlocal total, passed, skipped
        # B/E/G 依赖 pandas
        if tag in ("B", "E", "G") and not pandas_ok:
            print(f"[跳过] 套题{tag}-{kind}: 未安装 pandas")
            skipped += 1
            return
        file = ROOT / f"set_{tag}_{kind}.py"
        if not file.exists():
            print(f"[跳过] 文件不存在: {file}")
            skipped += 1
            return
        total += 1
        ok, out = run_file(file)
        status = "通过" if ok else "失败"
        print(f"\n=== 套题{tag}-{kind} -> {status} ===")
        if out.strip():
            print(out.strip())
        if ok:
            passed += 1

    for tag in sets:
        if want_blank:
            maybe_run(tag, "blank")
        if want_answers:
            maybe_run(tag, "answers")

    print("\n--- 总结 ---")
    print(f"总计: {total}，通过: {passed}，跳过: {skipped}，失败: {total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
