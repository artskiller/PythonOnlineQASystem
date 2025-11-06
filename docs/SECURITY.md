# 🔒 安全说明

## 概述

本项目的Web学习平台包含代码执行功能，为了保护系统安全，我们实施了多层安全防护措施。

---

## 🛡️ 安全架构

### 1. **代码沙箱（Code Sandbox）**

所有用户提交的代码都在隔离的沙箱环境中执行：

#### 特性
- ✅ **进程隔离** - 使用独立进程执行代码
- ✅ **资源限制** - 限制内存（256MB）和CPU时间（10秒）
- ✅ **模块白名单** - 只允许安全的Python模块
- ✅ **函数黑名单** - 禁止危险的内置函数
- ✅ **输出限制** - 限制输出大小（10KB）

#### 禁止的操作
- ❌ 文件系统访问（`open`, `file`, `pathlib`等）
- ❌ 网络访问（`socket`, `urllib`, `requests`等）
- ❌ 系统命令（`os.system`, `subprocess`等）
- ❌ 危险函数（`eval`, `exec`, `__import__`等）
- ❌ 进程/线程创建（`multiprocessing`, `threading`等）

#### 允许的模块
```python
# 标准库
math, random, datetime, collections, itertools, functools,
operator, string, re, json, decimal, fractions, statistics,
heapq, bisect, array, copy, pprint, enum, dataclasses, typing

# 数据科学（受限）
numpy, pandas, sklearn, jieba
```

---

### 2. **速率限制（Rate Limiting）**

防止滥用和DoS攻击：

- **每分钟限制**: 30次请求
- **每小时限制**: 500次请求
- **基于IP地址**: 每个IP独立计数
- **滑动窗口**: 精确的时间窗口控制

---

### 3. **输入验证**

- **代码长度限制**: 最大50KB
- **语法检查**: AST解析验证
- **模式匹配**: 检测危险代码模式
- **导入检查**: 验证所有import语句

---

### 4. **资源限制**

#### Unix/Linux系统
```python
- 内存限制: 256MB (RLIMIT_AS)
- CPU时间: 10秒 (RLIMIT_CPU)
- 执行超时: 10秒 (multiprocessing timeout)
```

#### Windows系统
```python
- 执行超时: 10秒 (multiprocessing timeout)
- 输出限制: 10KB
```

---

## 🚨 已知风险

### 1. **资源耗尽攻击**

**风险**: 用户可能尝试消耗大量内存或CPU

**缓解措施**:
- 进程级资源限制（Unix）
- 执行超时（所有平台）
- 速率限制
- 输出大小限制

### 2. **逻辑炸弹**

**风险**: 复杂的递归或循环可能绕过简单检查

**缓解措施**:
- CPU时间限制
- 进程隔离（崩溃不影响主进程）
- 超时机制

### 3. **信息泄露**

**风险**: 通过错误消息泄露系统信息

**缓解措施**:
- 过滤错误消息
- 禁止访问系统模块
- 受限的内置函数

---

## 🔧 部署建议

### 生产环境

1. **使用容器化部署**
   ```bash
   cd web/docker
   docker-compose up -d
   ```

2. **启用防火墙**
   - 只开放必要端口（80/443）
   - 限制入站连接

3. **使用反向代理**
   ```nginx
   # Nginx配置示例
   location /api/run {
       limit_req zone=api burst=5;
       proxy_pass http://localhost:8080;
   }
   ```

4. **监控和日志**
   - 启用安全日志
   - 监控异常请求
   - 设置告警

5. **定期更新**
   - 更新Python和依赖包
   - 审查安全补丁

### 开发环境

1. **本地测试**
   ```bash
   # 启用调试模式
   export FLASK_ENV=development
   python web/app.py
   ```

2. **安全测试**
   ```bash
   # 测试沙箱
   python -m pytest web/tests/test_security.py
   ```

---

## 📋 安全检查清单

### 部署前

- [ ] 确认沙箱已启用（`SANDBOX_ENABLED = True`）
- [ ] 确认速率限制已配置
- [ ] 确认资源限制已设置
- [ ] 审查允许的模块列表
- [ ] 测试危险代码被正确阻止
- [ ] 配置日志和监控
- [ ] 使用HTTPS（生产环境）
- [ ] 配置防火墙规则

### 运行时

- [ ] 监控CPU和内存使用
- [ ] 检查异常请求模式
- [ ] 审查安全日志
- [ ] 定期更新依赖

---

## 🐛 报告安全问题

如果您发现安全漏洞，请**不要**公开披露。请通过以下方式联系：

- 📧 Email: security@example.com
- 🔒 加密: 使用PGP密钥

我们会在24小时内响应，并在修复后公开致谢。

---

## 📚 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Sandboxing Python Code](https://docs.python.org/3/library/restricted.html)

---

## 📝 更新日志

### 2025-11-06
- ✅ 实施代码沙箱
- ✅ 添加速率限制
- ✅ 添加资源限制
- ✅ 添加输入验证
- ✅ 创建安全文档

---

**⚠️ 重要提示**: 

即使有这些安全措施，**永远不要**在不受信任的环境中运行用户代码。本系统适用于：

✅ **适用场景**:
- 教育和学习平台
- 内部培训系统
- 受控的开发环境

❌ **不适用场景**:
- 公开的互联网服务（未经额外加固）
- 处理敏感数据的系统
- 高安全要求的生产环境

---

**返回 [项目主页](../README.md) | [Web平台文档](../web/README.md)**

