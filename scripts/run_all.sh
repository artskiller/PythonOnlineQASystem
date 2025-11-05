#!/usr/bin/env bash
# 一键运行所有自检脚本（bash 版）
# 使用：
#   bash scripts/run_all.sh            # 默认运行答案版
#   bash scripts/run_all.sh blank      # 运行空白版
#   bash scripts/run_all.sh both       # 先空白后答案

set -euo pipefail

MODE="${1:-answers}"
if [[ "$MODE" != "answers" && "$MODE" != "blank" && "$MODE" != "both" ]]; then
  echo "用法: bash scripts/run_all.sh [answers|blank|both]" >&2
  exit 2
fi

exec python "$(dirname "$0")/../interview_exercises/run_all.py" --mode "$MODE"

