# 🔒 安全检查清单

本文档提供了部署和维护Web学习平台时的安全检查清单。

---

## 📋 部署前检查

### 代码安全

- [ ] **沙箱已启用**
  ```bash
  # 检查沙箱模块
  cd web && python -c "from security.sandbox import sandbox; print('✅ OK')"
  ```

- [ ] **安全测试通过**
  ```bash
  # 运行安全测试
  cd web && python tests/test_security.py
  ```

- [ ] **依赖已安装**
  ```bash
  # 安装依赖
  pip install -r web/requirements.txt
  ```

### 配置检查

- [ ] **资源限制已配置**
  - 检查 `web/security/config.py`
  - 确认 `MAX_MEMORY_MB = 256`
  - 确认 `MAX_CPU_TIME = 10`
  - 确认 `MAX_EXECUTION_TIME = 10`

- [ ] **速率限制已配置**
  - 检查 `web/security/rate_limiter.py`
  - 确认 `max_per_minute = 30`
  - 确认 `max_per_hour = 500`

- [ ] **危险模块已禁用**
  - 检查 `web/security/config.py`
  - 确认 `DANGEROUS_MODULES` 包含 os, subprocess, socket等
  - 确认 `ALLOW_FILE_IO = False`
  - 确认 `ALLOW_NETWORK = False`

### 环境检查

- [ ] **Python版本**
  ```bash
  python --version  # 建议 Python 3.8+
  ```

- [ ] **操作系统**
  - Unix/Linux: ✅ 完整资源限制
  - macOS: ⚠️  部分资源限制
  - Windows: ⚠️  仅超时保护

- [ ] **防火墙配置**
  - 只开放必要端口（80/443）
  - 限制入站连接
  - 配置IP白名单（可选）

---

## 🚀 运行时检查

### 应用状态

- [ ] **Web应用正常运行**
  ```bash
  curl http://localhost:8080/api/questions
  ```

- [ ] **沙箱功能正常**
  ```bash
  # 运行Web安全测试
  ./web/test_web_security.sh
  ```

### 安全功能

- [ ] **危险代码被阻止**
  - 测试 `import os` 被拒绝
  - 测试 `eval()` 被拒绝
  - 测试 `open()` 被拒绝

- [ ] **安全代码正常执行**
  - 测试 `print()` 正常
  - 测试 `import math` 正常
  - 测试数学运算正常

- [ ] **速率限制生效**
  - 快速发送30+请求
  - 确认返回429错误

- [ ] **资源限制生效**
  - 测试无限循环被终止
  - 测试大量输出被截断

---

## 🔧 生产环境检查

### 容器化部署

- [ ] **Docker配置**
  ```bash
  # 检查Dockerfile
  cat web/docker/Dockerfile
  
  # 检查docker-compose
  cat web/docker/docker-compose.yml
  ```

- [ ] **容器资源限制**
  - 设置内存限制（512MB-1GB）
  - 设置CPU限制（1-2核）
  - 设置网络隔离

### 反向代理

- [ ] **Nginx/Apache配置**
  - 配置速率限制
  - 配置请求大小限制
  - 配置超时设置

- [ ] **SSL/TLS**
  - 启用HTTPS
  - 配置SSL证书
  - 启用HSTS

### 监控和日志

- [ ] **日志配置**
  - 启用访问日志
  - 启用错误日志
  - 启用安全日志

- [ ] **监控指标**
  - CPU使用率
  - 内存使用率
  - 请求速率
  - 错误率

- [ ] **告警设置**
  - 高CPU使用率告警
  - 高内存使用率告警
  - 异常请求告警
  - 安全事件告警

---

## 🔄 定期维护检查

### 每周检查

- [ ] **审查访问日志**
  - 检查异常请求
  - 检查速率限制触发
  - 检查错误日志

- [ ] **运行安全测试**
  ```bash
  cd web && python tests/test_security.py
  ```

### 每月检查

- [ ] **更新依赖包**
  ```bash
  pip list --outdated
  pip install --upgrade -r web/requirements.txt
  ```

- [ ] **审查安全配置**
  - 检查 `web/security/config.py`
  - 根据需要调整限制

- [ ] **性能测试**
  - 测试并发请求
  - 测试资源使用
  - 优化配置

### 每季度检查

- [ ] **安全审计**
  - 审查代码变更
  - 检查新的安全漏洞
  - 更新安全策略

- [ ] **渗透测试**
  - 测试已知攻击向量
  - 测试新的攻击方式
  - 修复发现的问题

---

## 🚨 应急响应

### 发现安全问题

1. **立即行动**
   - [ ] 停止Web应用
   - [ ] 隔离受影响系统
   - [ ] 保存日志和证据

2. **评估影响**
   - [ ] 确定漏洞范围
   - [ ] 检查是否被利用
   - [ ] 评估数据泄露风险

3. **修复问题**
   - [ ] 开发补丁
   - [ ] 测试修复
   - [ ] 部署更新

4. **事后分析**
   - [ ] 编写事件报告
   - [ ] 更新安全策略
   - [ ] 改进监控

---

## 📞 联系方式

### 报告安全问题

- 📧 Email: security@example.com
- 🔒 PGP: [公钥链接]
- ⏱️ 响应时间: 24小时内

### 获取帮助

- 📖 文档: [docs/SECURITY.md](SECURITY.md)
- 💬 讨论: [GitHub Issues]
- 🐛 Bug报告: [GitHub Issues]

---

**最后更新**: 2025-11-06  
**版本**: 1.0  
**维护者**: pythonLearn Team

---

**返回 [安全说明](SECURITY.md) | [项目主页](../README.md)**

