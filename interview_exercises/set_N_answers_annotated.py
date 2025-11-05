"""
面试套题 N（异常与上下文）- 答案版
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable
import tempfile
import os
import time


@contextmanager
def safe_write(path: str):
    f = None
    try:
        f = open(path, "w", encoding="utf-8")
        yield f
    except Exception as e:
        raise RuntimeError("WRITE_FAIL:" + str(e))
    finally:
        if f:
            f.close()


def retry(max_times: int = 3, delay: float = 0.01):
    def deco(fn: Callable):
        def wrapper(*args, **kwargs):
            last = None
            for i in range(max_times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last = e
                    if i == max_times - 1:
                        break
                    time.sleep(delay)
            raise last
        return wrapper
    return deco


N3_ANSWER = "C"


def _run_self_tests():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        with safe_write(tmp.name) as f:
            f.write("ok")
        with open(tmp.name, "r", encoding="utf-8") as fr:
            assert fr.read() == "ok"
    finally:
        os.unlink(tmp.name)

    try:
        with safe_write("/root/forbidden/path.txt") as f:
            f.write("x")
        raised = False
    except Exception as e:
        raised = True
        assert str(e).startswith("WRITE_FAIL:")
    assert raised

    calls = {"n": 0}

    @retry(max_times=3, delay=0.001)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return 42

    assert flaky() == 42 and calls["n"] == 3
    assert N3_ANSWER == "C"
    print("[N 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

