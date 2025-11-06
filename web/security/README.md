# 🔒 安全模块

本目录包含Web学习平台的安全组件，用于保护系统免受恶意代码攻击。

---

## 📁 文件说明

### `sandbox.py`
**代码沙箱** - 核心安全组件

- 隔离执行用户代码
- AST语法检查
- 模块导入白名单/黑名单
- 资源限制（内存、CPU、输出）
- 进程隔离

### `rate_limiter.py`
**速率限制器** - 防止滥用

- 基于IP的请求限制
- 滑动窗口算法
- 每分钟/每小时限制
- 统计和监控

### `config.py`
**安全配置** - 可调整的安全参数

- 资源限制配置
- 模块白名单/黑名单
- 速率限制参数
- 日志配置

---

## 🚀 快速开始

### 基本使用

```python
from security.sandbox import sandbox

# 执行代码
result = sandbox.execute_safe("""
print('Hello, World!')
""", timeout=10)

if result["success"]:
    print(result["stdout"])
else:
    print(result["error"])
```

### 速率限制

```python
from security.rate_limiter import rate_limiter

# 检查是否允许请求
allowed, reason = rate_limiter.is_allowed(client_ip)
if not allowed:
    return {"error": reason}, 429
```

---

## 🧪 测试

运行安全测试：

```bash
# 从web目录运行
cd web
python tests/test_security.py

# 或使用pytest
pytest tests/test_security.py -v
```

---

## ⚙️ 配置

### 修改资源限制

编辑 `config.py`:

```python
MAX_MEMORY_MB = 256  # 最大内存
MAX_CPU_TIME = 10    # 最大CPU时间
MAX_EXECUTION_TIME = 10  # 最大执行时间
```

### 修改速率限制

编辑 `rate_limiter.py`:

```python
rate_limiter = RateLimiter(
    max_per_minute=30,  # 每分钟30次
    max_per_hour=500    # 每小时500次
)
```

### 添加允许的模块

编辑 `config.py`:

```python
SAFE_MODULES = {
    'math', 'random', 'datetime',
    # 添加新模块
    'your_safe_module',
}
```

---

## 🛡️ 安全特性

### 1. 进程隔离
- 每次执行使用独立进程
- 崩溃不影响主进程
- 自动清理资源

### 2. 资源限制
- **内存**: 256MB (Unix)
- **CPU时间**: 10秒 (Unix)
- **执行超时**: 10秒 (所有平台)
- **输出大小**: 10KB

### 3. 代码检查
- AST语法分析
- 导入语句验证
- 危险函数检测
- 代码模式匹配

### 4. 速率限制
- IP级别限制
- 滑动窗口算法
- 自动清理过期记录

---

## ⚠️ 已知限制

### Unix/Linux
- ✅ 完整的资源限制（RLIMIT）
- ✅ 信号超时（SIGALRM）
- ✅ 内存限制

### Windows
- ⚠️  不支持RLIMIT
- ✅ 进程超时
- ✅ 输出限制

### macOS
- ✅ 部分资源限制
- ✅ 进程超时
- ⚠️  某些限制可能不生效

---

## 🔧 故障排除

### 问题：沙箱未启用

**症状**: 看到警告 "安全沙箱未启用"

**解决**:
```bash
# 确保在web目录
cd web

# 检查security模块
python -c "from security.sandbox import sandbox; print('OK')"

# 如果失败，检查Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题：multiprocessing错误

**症状**: "RuntimeError: context has already been set"

**解决**:
```python
# 在主程序开头添加
if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
```

### 问题：资源限制不生效

**症状**: Windows上内存限制无效

**说明**: Windows不支持resource模块，只能使用进程超时

---

## 📚 参考

- [Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Python resource](https://docs.python.org/3/library/resource.html)
- [AST - Abstract Syntax Trees](https://docs.python.org/3/library/ast.html)

---

**返回 [Web应用文档](../README.md) | [安全说明](../../docs/SECURITY.md)**

