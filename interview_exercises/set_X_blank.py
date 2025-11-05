"""
专项套题 X（审计日志与轮转，纯标准库）- 空白版

要求：
- 写入事件为一行 JSON 文本
- 超过 max_bytes 后轮转：audit.log -> audit.log.1；保留 backups 个，超过则删除最旧
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
        # TODO：从最大的序号开始往后移动，最后将当前文件改名为 .1
        pass

    def write(self, event: dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        line = json.dumps(event, ensure_ascii=False) + "\n"
        # TODO：若写入后超过 max_bytes，则先 rotate 再写
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)


def _run_self_tests():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "audit.log")
        lg = AuditLogger(p, max_bytes=50, backups=2)
        for i in range(20):
            lg.write({"i": i, "msg": "x" * 10})
        # 至少应有当前文件与 .1 存在
        assert os.path.exists(p) and os.path.exists(p + ".1")
    print("[X 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

