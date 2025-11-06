"""
安全配置 - 可根据部署环境调整
"""

# 资源限制
MAX_MEMORY_MB = 256  # 最大内存（MB）
MAX_CPU_TIME = 10    # 最大CPU时间（秒）
MAX_EXECUTION_TIME = 10  # 最大执行时间（秒）
MAX_OUTPUT_SIZE = 10000  # 最大输出大小（字节）
MAX_CODE_SIZE = 50000    # 最大代码大小（字节）

# 并发限制
MAX_CONCURRENT_EXECUTIONS = 5  # 最大并发执行数

# 速率限制
RATE_LIMIT_PER_MINUTE = 30  # 每分钟最大请求数
RATE_LIMIT_PER_HOUR = 500   # 每小时最大请求数

# 安全模式
STRICT_MODE = True  # 严格模式：禁止所有未明确允许的操作
ALLOW_FILE_IO = False  # 是否允许文件I/O
ALLOW_NETWORK = False  # 是否允许网络访问
ALLOW_SUBPROCESS = False  # 是否允许子进程

# 允许的模块白名单
SAFE_MODULES = {
    # 标准库
    'math', 'random', 'datetime', 'collections', 'itertools',
    'functools', 'operator', 'string', 're', 'json', 'decimal',
    'fractions', 'statistics', 'heapq', 'bisect', 'array',
    'copy', 'pprint', 'enum', 'dataclasses', 'typing',
    
    # 数据科学（受限）
    'numpy', 'pandas', 'sklearn', 'jieba',
    
    # 可选：根据需要添加
    # 'matplotlib', 'seaborn', 'scipy',
}

# 危险模块黑名单
DANGEROUS_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
    'shutil', 'pathlib', 'glob', 'tempfile', 'pickle', 'shelve',
    'importlib', '__import__', 'eval', 'exec', 'compile',
    'open', 'file', 'input', 'raw_input',
    'multiprocessing', 'threading', 'asyncio',
    'ctypes', 'cffi', 'pty', 'fcntl', 'resource',
    'webbrowser', 'http', 'ftplib', 'smtplib', 'telnetlib',
}

# 危险函数黑名单
DANGEROUS_BUILTINS = {
    '__import__', 'eval', 'exec', 'compile', 'open', 'file',
    'input', 'raw_input', 'execfile', 'reload', 'vars', 'dir',
    'globals', 'locals', 'delattr', 'setattr', 'getattr',
}

# 日志配置
ENABLE_SECURITY_LOGGING = True  # 启用安全日志
LOG_VIOLATIONS = True  # 记录安全违规
LOG_EXECUTIONS = False  # 记录所有执行（可能产生大量日志）

