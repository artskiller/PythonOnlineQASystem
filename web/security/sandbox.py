#!/usr/bin/env python3
"""
安全沙箱模块 - 限制代码执行权限
使用RestrictedPython和资源限制来防止恶意代码执行

跨平台支持:
- Linux: 完整的资源限制 (RLIMIT)
- macOS: 部分资源限制
- Windows: 仅超时保护
"""

import sys
import ast
import platform
import multiprocessing
import warnings
from typing import Dict, Any, Tuple
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# 平台特定导入
if sys.platform != 'win32':
    import resource
    import signal
else:
    resource = None
    signal = None


class SecurityError(Exception):
    """安全检查失败异常"""
    pass


class CodeSandbox:
    """代码沙箱 - 安全执行用户代码"""
    
    # 危险模块黑名单
    DANGEROUS_MODULES = {
        'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
        'shutil', 'pathlib', 'glob', 'tempfile', 'pickle', 'shelve',
        'importlib', '__import__', 'eval', 'exec', 'compile',
        'open', 'file', 'input', 'raw_input',
        'multiprocessing', 'threading', 'asyncio',
        'ctypes', 'cffi', 'pty', 'fcntl', 'resource',
    }
    
    # 危险内置函数黑名单
    DANGEROUS_BUILTINS = {
        '__import__', 'eval', 'exec', 'compile', 'open', 'file',
        'input', 'raw_input', 'execfile', 'reload', 'vars', 'dir',
        'globals', 'locals', 'delattr', 'setattr', 'getattr',
    }
    
    # 允许的安全模块
    SAFE_MODULES = {
        'math', 'random', 'datetime', 'collections', 'itertools',
        'functools', 'operator', 'string', 're', 'json', 'decimal',
        'fractions', 'statistics', 'heapq', 'bisect', 'array',
        'copy', 'pprint', 'enum', 'dataclasses', 'typing',
        # 数据科学库（受限）
        'numpy', 'pandas', 'sklearn', 'jieba',
    }
    
    # 资源限制
    MAX_MEMORY_MB = 256  # 最大内存256MB
    MAX_CPU_TIME = 10    # 最大CPU时间10秒
    MAX_OUTPUT_SIZE = 10000  # 最大输出10KB
    
    def __init__(self):
        self.violations = []
        self.platform = sys.platform

        # Windows平台警告
        if self.platform == 'win32':
            warnings.warn(
                "⚠️  Windows平台不支持完整的资源限制（内存、CPU）。\n"
                "   建议使用WSL2或Linux环境以获得完整的安全保护。\n"
                "   当前仅提供: 超时保护、输出限制、代码检查。",
                RuntimeWarning,
                stacklevel=2
            )
    
    def check_imports(self, code: str) -> bool:
        """检查导入语句是否安全"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise SecurityError(f"语法错误: {e}")

        for node in ast.walk(tree):
            # 检查 import 语句
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split('.')[0]
                    if module in self.DANGEROUS_MODULES:
                        self.violations.append(f"禁止导入危险模块: {module}")
                    # 注意：不检查是否在SAFE_MODULES中，只检查是否在黑名单

            # 检查 from ... import 语句
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split('.')[0]
                    if module in self.DANGEROUS_MODULES:
                        self.violations.append(f"禁止导入危险模块: {module}")

            # 检查函数调用
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.DANGEROUS_BUILTINS:
                        self.violations.append(f"禁止使用危险函数: {node.func.id}")

        return len(self.violations) == 0
    
    def check_code_patterns(self, code: str) -> bool:
        """检查代码中的危险模式"""
        dangerous_patterns = [
            ('__', '禁止使用双下划线属性'),
            ('exec(', '禁止使用exec'),
            ('eval(', '禁止使用eval'),
            ('compile(', '禁止使用compile'),
            ('open(', '禁止使用open'),
            ('file(', '禁止使用file'),
            ('input(', '禁止使用input'),
            ('__import__', '禁止使用__import__'),
            ('subprocess', '禁止使用subprocess'),
            ('os.system', '禁止使用os.system'),
            ('os.popen', '禁止使用os.popen'),
        ]
        
        for pattern, message in dangerous_patterns:
            if pattern in code:
                self.violations.append(message)
        
        return len(self.violations) == 0
    
    def set_resource_limits(self):
        """
        设置资源限制（平台相关）

        - Linux: 完整的RLIMIT支持
        - macOS: 部分RLIMIT支持（某些限制可能被忽略）
        - Windows: 不支持（跳过）
        """
        if sys.platform == 'win32':
            # Windows不支持resource模块
            return

        if resource is None:
            return

        try:
            # 限制内存（Linux完全支持，macOS可能部分支持）
            try:
                resource.setrlimit(
                    resource.RLIMIT_AS,
                    (self.MAX_MEMORY_MB * 1024 * 1024, self.MAX_MEMORY_MB * 1024 * 1024)
                )
            except (ValueError, OSError) as e:
                # macOS可能不支持RLIMIT_AS
                if sys.platform == 'darwin':
                    pass  # macOS: 忽略内存限制错误
                else:
                    raise

            # 限制CPU时间（Unix系统都支持）
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (self.MAX_CPU_TIME, self.MAX_CPU_TIME)
            )
        except Exception as e:
            # 降级处理：即使资源限制失败，仍然依赖超时机制
            pass
    
    def execute_safe(self, code: str, timeout: int = 10) -> Dict[str, Any]:
        """
        在安全环境中执行代码
        
        Args:
            code: 要执行的Python代码
            timeout: 超时时间（秒）
        
        Returns:
            执行结果字典
        """
        # 1. 安全检查
        self.violations = []
        
        if not self.check_imports(code):
            return {
                "success": False,
                "error": "安全检查失败",
                "violations": self.violations
            }
        
        if not self.check_code_patterns(code):
            return {
                "success": False,
                "error": "代码包含危险模式",
                "violations": self.violations
            }
        
        # 2. 使用多进程隔离执行
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=self._run_in_process,
            args=(code, queue)
        )
        
        process.start()
        process.join(timeout=timeout)
        
        if process.is_alive():
            process.terminate()
            process.join()
            return {
                "success": False,
                "error": f"代码执行超时（超过{timeout}秒）"
            }
        
        # 3. 获取执行结果
        if not queue.empty():
            return queue.get()
        else:
            return {
                "success": False,
                "error": "代码执行失败，未返回结果"
            }

    def _run_in_process(self, code: str, queue: multiprocessing.Queue):
        """
        在独立进程中执行代码

        平台差异:
        - Unix: 使用SIGALRM信号超时
        - Windows: 依赖multiprocessing的超时机制
        """
        try:
            # 设置资源限制（Unix系统）
            self.set_resource_limits()

            # 设置超时信号（仅Unix系统）
            if sys.platform != 'win32' and signal is not None:
                signal.signal(signal.SIGALRM, self._timeout_handler)
                signal.alarm(self.MAX_CPU_TIME)

            # 创建受限的全局命名空间（允许导入）
            safe_globals = {
                '__builtins__': self._get_safe_builtins(),
                '__name__': '__main__',
                '__doc__': None,
            }

            # 捕获输出
            stdout_capture = StringIO()
            stderr_capture = StringIO()

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # 执行代码（允许导入，但已经通过AST检查过）
                exec(code, safe_globals, safe_globals)

            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()

            # 限制输出大小
            if len(stdout) > self.MAX_OUTPUT_SIZE:
                stdout = stdout[:self.MAX_OUTPUT_SIZE] + "\n... (输出被截断)"
            if len(stderr) > self.MAX_OUTPUT_SIZE:
                stderr = stderr[:self.MAX_OUTPUT_SIZE] + "\n... (输出被截断)"

            queue.put({
                "success": True,
                "stdout": stdout,
                "stderr": stderr,
                "returncode": 0
            })

        except MemoryError:
            queue.put({
                "success": False,
                "error": "内存超限（超过256MB）"
            })

        except Exception as e:
            queue.put({
                "success": False,
                "error": f"执行错误: {type(e).__name__}: {str(e)}",
                "stderr": str(e)
            })

    def _timeout_handler(self, signum, frame):
        """超时处理器（仅Unix系统使用）"""
        raise TimeoutError("CPU时间超限")

    def get_platform_info(self) -> Dict[str, Any]:
        """
        获取平台信息和安全能力

        Returns:
            平台信息字典
        """
        capabilities = {
            'platform': sys.platform,
            'platform_name': platform.system(),
            'python_version': sys.version.split()[0],
            'multiprocessing': True,
            'timeout': True,
            'output_limit': True,
            'ast_check': True,
            'resource_limit': False,
            'signal_timeout': False,
        }

        if sys.platform != 'win32':
            capabilities['resource_limit'] = resource is not None
            capabilities['signal_timeout'] = signal is not None

        return capabilities

    def _get_safe_builtins(self) -> dict:
        """获取安全的内置函数"""
        import builtins

        safe_builtins = {}

        # 允许的内置函数
        allowed = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'complex', 'dict', 'divmod',
            'enumerate', 'filter', 'float', 'format', 'frozenset', 'hash',
            'hex', 'id', 'int', 'isinstance', 'issubclass', 'iter', 'len',
            'list', 'map', 'max', 'min', 'next', 'object', 'oct', 'ord',
            'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round',
            'set', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
            'tuple', 'type', 'zip',
            # 异常类
            'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'AttributeError', 'RuntimeError', 'StopIteration', 'ZeroDivisionError',
        }

        for name in allowed:
            if hasattr(builtins, name):
                safe_builtins[name] = getattr(builtins, name)

        # 添加受限的__import__（通过AST已经检查过）
        safe_builtins['__import__'] = __import__

        return safe_builtins


# 全局沙箱实例
sandbox = CodeSandbox()


