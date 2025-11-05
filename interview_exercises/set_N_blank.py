"""
面试套题 N（异常与上下文）- 空白版

题型包含：上下文管理器、异常包装、重试装饰器、选择题
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable
import tempfile
import os
import time


# 上下文 N1：安全写文件，失败时仍确保关闭，且异常信息前缀为 "WRITE_FAIL:" 后再抛出
@contextmanager
def safe_write(path: str):
    f = None
    try:
        f = open(path, "w", encoding="utf-8")
        yield f
    except Exception as e:
        # TODO：包装异常并抛出
        raise
    finally:
        if f:
            f.close()


# 装饰器 N2：带最大尝试次数与固定间隔的重试
def retry(max_times: int = 3, delay: float = 0.01):
    def deco(fn: Callable):
        def wrapper(*args, **kwargs):
            # TODO：失败则重试，达到上限后抛出
            return fn(*args, **kwargs)
        return wrapper
    return deco


# 选择题 N3：关于 try/except/else/finally 哪项正确？
# A. else 在 except 执行后执行
# B. finally 仅在无异常时执行
# C. else 在 try 块不抛异常时执行
# D. except 会屏蔽 finally
N3_ANSWER = "__"


def _run_self_tests():
    # N1：成功写
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        with safe_write(tmp.name) as f:
            f.write("ok")
        with open(tmp.name, "r", encoding="utf-8") as fr:
            assert fr.read() == "ok"
    finally:
        os.unlink(tmp.name)

    # N1：失败时抛出带前缀
    try:
        with safe_write("/root/forbidden/path.txt") as f:
            f.write("x")
        raised = False
    except Exception as e:
        raised = True
        assert str(e).startswith("WRITE_FAIL:")
    assert raised

    # N2：重试
    calls = {"n": 0}

    @retry(max_times=3, delay=0.001)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return 42

    assert flaky() == 42 and calls["n"] == 3

    # N3
    assert N3_ANSWER in {"A", "B", "C", "D"}
    assert N3_ANSWER == "C"

    print("[N 空白版] 自检断言：全部通过（请完善实现与答案）")


if __name__ == "__main__":
    _run_self_tests()

