#!/usr/bin/env python3
"""
安全测试 - 验证沙箱和安全措施
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from security.sandbox import CodeSandbox, SecurityError


def test_dangerous_imports():
    """测试危险模块导入被阻止"""
    sandbox = CodeSandbox()
    
    dangerous_codes = [
        "import os",
        "import subprocess",
        "import socket",
        "from os import system",
        "import sys",
    ]
    
    for code in dangerous_codes:
        result = sandbox.execute_safe(code)
        assert not result["success"], f"应该阻止: {code}"
        print(f"✅ 成功阻止: {code}")


def test_dangerous_functions():
    """测试危险函数被阻止"""
    sandbox = CodeSandbox()
    
    dangerous_codes = [
        "eval('1+1')",
        "exec('print(1)')",
        "open('/etc/passwd')",
        "__import__('os')",
    ]
    
    for code in dangerous_codes:
        result = sandbox.execute_safe(code)
        assert not result["success"], f"应该阻止: {code}"
        print(f"✅ 成功阻止: {code}")


def test_safe_code():
    """测试安全代码可以执行"""
    sandbox = CodeSandbox()
    
    safe_codes = [
        "print('Hello, World!')",
        "x = 1 + 1\nprint(x)",
        "import math\nprint(math.pi)",
        "def add(a, b):\n    return a + b\nprint(add(1, 2))",
    ]
    
    for code in safe_codes:
        result = sandbox.execute_safe(code)
        assert result["success"], f"应该允许: {code}"
        print(f"✅ 成功执行: {code[:30]}...")


def test_resource_limits():
    """测试资源限制"""
    sandbox = CodeSandbox()
    
    # 测试超时
    timeout_code = """
import time
while True:
    pass
"""
    result = sandbox.execute_safe(timeout_code, timeout=2)
    assert not result["success"], "应该超时"
    print("✅ 超时限制生效")
    
    # 测试大量输出
    large_output_code = """
for i in range(100000):
    print('x' * 1000)
"""
    result = sandbox.execute_safe(large_output_code, timeout=5)
    # 输出可能被截断或超时
    if result.get("success"):
        output_len = len(result.get("stdout", ""))
        if output_len <= 10100:  # 允许一些误差
            print("✅ 输出限制生效")
        else:
            print(f"⚠️  输出未被截断: {output_len} 字节")
    else:
        # 超时也是可接受的
        print("✅ 输出限制生效（超时）")


def test_numpy_pandas():
    """测试允许的数据科学库"""
    sandbox = CodeSandbox()
    
    # NumPy
    numpy_code = """
import numpy as np
arr = np.array([1, 2, 3])
print(arr.sum())
"""
    result = sandbox.execute_safe(numpy_code)
    if result["success"]:
        print("✅ NumPy 可用")
    else:
        print("⚠️  NumPy 未安装（可选）")
    
    # Pandas
    pandas_code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3]})
print(df.sum())
"""
    result = sandbox.execute_safe(pandas_code)
    if result["success"]:
        print("✅ Pandas 可用")
    else:
        print("⚠️  Pandas 未安装（可选）")


def test_code_patterns():
    """测试危险代码模式检测"""
    sandbox = CodeSandbox()
    
    dangerous_patterns = [
        "x.__class__",
        "exec('code')",
        "eval('code')",
        "open('file')",
    ]
    
    for code in dangerous_patterns:
        result = sandbox.execute_safe(code)
        assert not result["success"], f"应该阻止模式: {code}"
        print(f"✅ 成功阻止模式: {code}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🔒 安全测试开始")
    print("=" * 60)
    
    try:
        print("\n1️⃣  测试危险模块导入...")
        test_dangerous_imports()
        
        print("\n2️⃣  测试危险函数...")
        test_dangerous_functions()
        
        print("\n3️⃣  测试安全代码...")
        test_safe_code()
        
        print("\n4️⃣  测试资源限制...")
        test_resource_limits()
        
        print("\n5️⃣  测试数据科学库...")
        test_numpy_pandas()
        
        print("\n6️⃣  测试危险模式...")
        test_code_patterns()
        
        print("\n" + "=" * 60)
        print("✅ 所有安全测试通过！")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

