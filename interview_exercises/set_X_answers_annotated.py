"""
专项套题 X（审计日志与轮转，纯标准库）- 答案版
"""

from __future__ import annotations

import json
import os
import tempfile
from typing import Any


class AuditLogger:
    def __init__(self, path: str, max_bytes: int = 128, backups: int = 2) -> None:
        self.path = path
        self.max_bytes = max_bytes
        self.backups = backups

    def _rotate(self) -> None:
        # 删除最旧
        oldest = f"{self.path}.{self.backups}"
        if os.path.exists(oldest):
            os.remove(oldest)
        # 向后移动
        for i in range(self.backups - 1, 0, -1):
            src = f"{self.path}.{i}"
            dst = f"{self.path}.{i+1}"
            if os.path.exists(src):
                os.replace(src, dst)
        # 当前 -> .1
        if os.path.exists(self.path):
            os.replace(self.path, f"{self.path}.1")

    def write(self, event: dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        line = json.dumps(event, ensure_ascii=False) + "\n"
        # 计算写入后是否超限
        cur_size = os.path.getsize(self.path) if os.path.exists(self.path) else 0
        if cur_size + len(line.encode("utf-8")) > self.max_bytes:
            self._rotate()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)


def _run_self_tests():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "audit.log")
        lg = AuditLogger(p, max_bytes=50, backups=2)
        for i in range(20):
            lg.write({"i": i, "msg": "x" * 10})
        assert os.path.exists(p) and os.path.exists(p + ".1")
    print("[X 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

