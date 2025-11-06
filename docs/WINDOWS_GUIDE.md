# 🪟 Windows 用户指南

本文档专门为Windows用户提供pythonLearn项目的安装和使用指南。

---

## ⚠️ 重要提示

Windows平台对本项目的支持**有限**，主要限制：

| 功能 | Windows支持 | 说明 |
|------|------------|------|
| Python学习 | ✅ 完全支持 | 核心学习功能正常 |
| Web平台 | ✅ 基本支持 | 界面和基本功能正常 |
| 代码沙箱 | ⚠️ 受限 | 无法限制内存和CPU |
| Shell脚本 | ❌ 不支持 | 需要Git Bash或WSL |
| Makefile | ❌ 不支持 | 使用`setup.py`替代 |

**推荐方案**: 使用WSL2获得完整功能（见下文）

---

## 🎯 推荐方案：WSL2（强烈推荐）

### 为什么选择WSL2？

- ✅ 完整的Linux环境
- ✅ 100%功能支持
- ✅ 完整的安全沙箱
- ✅ 原生Shell脚本支持
- ✅ 更好的性能

### 安装WSL2

#### 1. 启用WSL2

打开PowerShell（管理员权限）：

```powershell
# 启用WSL
wsl --install

# 或者手动启用
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启电脑
```

#### 2. 安装Ubuntu

```powershell
# 安装Ubuntu 22.04
wsl --install -d Ubuntu-22.04

# 或从Microsoft Store安装
# 搜索 "Ubuntu" 并安装
```

#### 3. 设置Ubuntu

首次启动会要求创建用户：

```bash
# 输入用户名和密码
# 然后更新系统
sudo apt update
sudo apt upgrade -y
```

#### 4. 在WSL中使用项目

```bash
# 访问Windows文件系统
cd /mnt/c/Users/YourName/Documents/pythonLearn

# 或者克隆到WSL文件系统（推荐，性能更好）
cd ~
git clone <repository-url>
cd pythonLearn

# 安装Python
sudo apt install python3 python3-pip python3-venv

# 初始化项目
make setup

# 启动Web平台
make web
```

#### 5. 访问Web平台

在Windows浏览器中访问：
```
http://localhost:8080
```

---

## 💻 方案B：原生Windows

如果不想使用WSL2，可以在原生Windows上运行（功能受限）。

### 前置要求

1. **Python 3.8+**
   - 下载: https://www.python.org/downloads/
   - ⚠️ 安装时勾选 "Add Python to PATH"

2. **Git for Windows**（可选，用于Git Bash）
   - 下载: https://git-scm.com/download/win

### 安装步骤

#### 使用PowerShell

```powershell
# 1. 克隆项目
git clone <repository-url>
cd pythonLearn

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
.venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt
pip install -r web\requirements.txt

# 5. 启动Web平台
cd web
python app.py
```

#### 使用setup.py（推荐）

```powershell
# 1. 克隆项目
git clone <repository-url>
cd pythonLearn

# 2. 初始化项目
python setup.py setup

# 3. 启动Web平台
python setup.py web
```

### 使用Git Bash

如果安装了Git for Windows，可以使用Git Bash：

```bash
# Git Bash支持大部分Linux命令
cd /c/path/to/pythonLearn

# 可以使用make命令
make setup
make web
```

---

## ⚠️ Windows限制说明

### 1. 安全沙箱受限

**问题**: Windows不支持`resource`模块

**影响**:
- ❌ 无法限制内存使用
- ❌ 无法限制CPU时间
- ✅ 仍有超时保护（10秒）
- ✅ 仍有输出限制（10KB）
- ✅ 仍有代码检查（AST）

**风险**:
- 恶意代码可能消耗大量内存
- 恶意代码可能消耗大量CPU

**建议**:
- 仅在受信任的环境中使用
- 不要在公网暴露Web平台
- 定期监控系统资源

### 2. 路径分隔符

Windows使用反斜杠`\`，Linux使用正斜杠`/`

**解决方案**: 项目已使用`pathlib.Path`处理，自动兼容

```python
# ✅ 正确 - 跨平台
from pathlib import Path
file_path = Path('web') / 'app.py'

# ❌ 错误 - 仅Linux
file_path = 'web/app.py'
```

### 3. 行尾符

Windows使用`\r\n`，Linux使用`\n`

**解决方案**: Git自动处理

```bash
# 配置Git自动转换
git config --global core.autocrlf true
```

### 4. 颜色输出

Windows CMD不支持ANSI颜色代码

**解决方案**: 项目已集成`colorama`库

```python
# 自动在Windows上启用颜色支持
if sys.platform == 'win32':
    import colorama
    colorama.init()
```

---

## 🧪 测试

### 运行安全测试

```powershell
# PowerShell
python setup.py test

# 或直接运行
python web\tests\test_security.py
```

### 预期结果

```
✅ 21/21 测试通过

⚠️  警告: Windows平台不支持完整的资源限制
   建议使用WSL2或Linux环境以获得完整的安全保护
```

---

## 🔧 常见问题

### Q1: 提示"python不是内部或外部命令"

**原因**: Python未添加到PATH

**解决方案**:
1. 重新安装Python，勾选"Add Python to PATH"
2. 或手动添加到PATH：
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 添加Python安装路径到PATH

### Q2: pip安装依赖失败

**原因**: 网络问题或权限问题

**解决方案**:
```powershell
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用管理员权限
# 右键PowerShell → 以管理员身份运行
```

### Q3: 端口8080被占用

**原因**: 其他程序占用端口

**解决方案**:
```powershell
# 查找占用端口的程序
netstat -ano | findstr :8080

# 结束进程（替换PID）
taskkill /PID <PID> /F

# 或修改端口
# 编辑 web/app.py，修改端口号
```

### Q4: 虚拟环境激活失败

**原因**: PowerShell执行策略限制

**解决方案**:
```powershell
# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 然后激活虚拟环境
.venv\Scripts\activate
```

---

## 📚 相关文档

- [跨平台兼容性指南](PLATFORM_COMPATIBILITY.md)
- [安全说明](SECURITY.md)
- [项目主页](../README.md)

---

## 💡 最佳实践

### 开发环境

- ✅ 使用WSL2（推荐）
- ✅ 使用Git Bash
- ✅ 使用VS Code + Remote WSL扩展

### 生产环境

- ❌ 不推荐在Windows上部署生产环境
- ✅ 使用Linux服务器
- ✅ 使用Docker容器

---

**🎉 祝学习愉快！**

如有问题，请查看 [常见问题](FAQ.md) 或提交Issue。

