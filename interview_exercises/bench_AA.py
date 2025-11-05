"""
并发版 AA 压测脚本（模拟大量小文件）

用法：
  python interview_exercises/bench_AA.py --files 200 --rows 5 --workers 8

说明：
- 在临时目录生成 N 个小 CSV 文件，每个包含 R 行；
- 调用 set_AA_answers.run_pipeline 并统计耗时与吞吐。
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import random
import tempfile
import time
from typing import List, Dict


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", type=int, default=200)
    ap.add_argument("--rows", type=int, default=5)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv)

    # 延迟导入，便于直接运行脚本
    from set_AA_answers import run_pipeline

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    lg = logging.getLogger("bench_aa")

    with tempfile.TemporaryDirectory() as d:
        # 生成文件
        for i in range(args.files):
            path = os.path.join(d, f"f_{i:05d}.csv")
            with open(path, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["code", "number", "amount", "rate", "date", "dept"])
                for j in range(args.rows):
                    amt = random.choice([113, 106])
                    rate = 0.13 if amt == 113 else 0.06
                    dt = random.choice(["2024-03-01", "2024-03-15", "2024-04-01"])  # 两个期间
                    dept = random.choice(["A", "B", "C"])  # 多部门
                    w.writerow([f"c{i}", f"n{j}", amt, rate, dt, dept])

        t0 = time.perf_counter()
        rep = run_pipeline(d, lg, max_workers=args.workers)
        dt = time.perf_counter() - t0
        total_rows = args.files * args.rows
        print(f"files={args.files} rows={total_rows} workers={args.workers} time={dt:.3f}s throughput={total_rows/dt:.1f} rows/s")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

