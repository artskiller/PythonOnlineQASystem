# 🌍 跨平台兼容性指南

本文档说明pythonLearn项目在不同操作系统平台上的兼容性问题及解决方案。

---

## 📊 平台支持概览

| 平台 | 支持状态 | 核心功能 | Web平台 | 安全沙箱 | 备注 |
|------|---------|---------|---------|---------|------|
| **Linux** | ✅ 完全支持 | ✅ | ✅ | ✅ 完整 | 推荐生产环境 |
| **macOS** | ✅ 完全支持 | ✅ | ✅ | ⚠️ 部分 | 开发环境推荐 |
| **Windows** | ⚠️ 部分支持 | ✅ | ✅ | ⚠️ 受限 | 需要额外配置 |
| **WSL2** | ✅ 完全支持 | ✅ | ✅ | ✅ 完整 | Windows最佳选择 |

---

## 🐧 Linux

### 支持状态
✅ **完全支持** - 推荐用于生产环境

### 特性
- ✅ 完整的资源限制（RLIMIT）
- ✅ 信号超时（SIGALRM）
- ✅ 内存限制
- ✅ CPU时间限制
- ✅ 所有Shell脚本正常工作

### 测试的发行版
- Ubuntu 20.04/22.04 LTS ✅
- Debian 11/12 ✅
- CentOS 7/8 ✅
- Fedora 36+ ✅
- Arch Linux ✅

### 安装步骤

```bash
# 1. 安装Python 3.8+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 2. 克隆项目
git clone <repository-url>
cd pythonLearn

# 3. 初始化项目
make setup

# 4. 启动Web平台
make web
```

---

## 🍎 macOS

### 支持状态
✅ **完全支持** - 推荐用于开发环境

### 特性
- ✅ 基本资源限制
- ✅ 进程超时
- ⚠️ 某些RLIMIT可能不生效
- ✅ 所有Shell脚本正常工作

### 测试的版本
- macOS 12 (Monterey) ✅
- macOS 13 (Ventura) ✅
- macOS 14 (Sonoma) ✅

### 已知问题

#### 1. resource.RLIMIT_AS 可能不生效
**问题**: macOS上内存限制可能被忽略

**解决方案**: 依赖进程超时和输出限制
```python
# 已在sandbox.py中实现
if sys.platform == 'darwin':
    # macOS: 主要依赖超时机制
    pass
```

#### 2. Bash版本较旧
**问题**: macOS默认使用Bash 3.x

**解决方案**: 
```bash
# 选项1: 升级Bash
brew install bash

# 选项2: 使用zsh（macOS默认）
# 脚本已兼容zsh
```

### 安装步骤

```bash
# 1. 安装Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装Python 3.8+
brew install python@3.11

# 3. 克隆项目
git clone <repository-url>
cd pythonLearn

# 4. 初始化项目
make setup

# 5. 启动Web平台
make web
```

---

## 🪟 Windows

### 支持状态
⚠️ **部分支持** - 需要额外配置

### 特性
- ✅ Python核心功能
- ✅ Web平台基本功能
- ❌ 不支持resource模块
- ❌ 不支持SIGALRM信号
- ⚠️ Shell脚本需要Git Bash或WSL
- ✅ 进程超时保护

### 限制说明

#### 1. 资源限制不可用
**问题**: Windows不支持`resource`模块

**影响**: 
- ❌ 无法限制内存使用
- ❌ 无法限制CPU时间

**缓解措施**:
- ✅ 进程超时仍然有效（10秒）
- ✅ 输出大小限制仍然有效（10KB）
- ✅ AST代码检查仍然有效

#### 2. Shell脚本不可用
**问题**: Windows CMD不支持Bash脚本

**解决方案**: 使用Python脚本替代（见下文）

### 推荐方案

#### 方案A: 使用WSL2（强烈推荐）

```powershell
# 1. 启用WSL2
wsl --install

# 2. 安装Ubuntu
wsl --install -d Ubuntu-22.04

# 3. 在WSL中使用
wsl
cd /mnt/c/path/to/pythonLearn
make setup
make web
```

#### 方案B: 使用Git Bash

```bash
# 1. 安装Git for Windows（包含Git Bash）
# 下载: https://git-scm.com/download/win

# 2. 在Git Bash中运行
cd /c/path/to/pythonLearn
make setup
make web
```

#### 方案C: 纯Python方式（无需Shell）

```powershell
# 1. 安装Python 3.8+
# 下载: https://www.python.org/downloads/

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
pip install -r web\requirements.txt

# 4. 启动Web平台
cd web
python app.py
```

---

## 🔧 跨平台兼容性修复

### 已实施的修复

#### 1. 平台检测
```python
import sys
import platform

# 检测操作系统
if sys.platform == 'win32':
    # Windows特定代码
elif sys.platform == 'darwin':
    # macOS特定代码
else:
    # Linux/Unix特定代码
```

#### 2. 资源限制兼容性
```python
def set_resource_limits(self):
    """设置资源限制（仅Unix系统）"""
    if sys.platform != 'win32':
        try:
            import resource
            resource.setrlimit(...)
        except Exception:
            pass  # 降级处理
```

#### 3. 信号处理兼容性
```python
if sys.platform != 'win32':
    import signal
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
```

#### 4. 路径处理
```python
from pathlib import Path

# 使用Path对象，自动处理不同平台的路径分隔符
base_dir = Path(__file__).parent
data_file = base_dir / 'data' / 'file.txt'
```

---

## 📝 待修复的兼容性问题

### 高优先级

1. **Makefile在Windows上不可用**
   - 影响: Windows用户无法使用`make`命令
   - 解决方案: 创建`setup.py`或`tasks.py`

2. **Shell脚本在Windows上不可用**
   - 影响: `organize_exercises.sh`等脚本无法运行
   - 解决方案: 转换为Python脚本

3. **Windows安全沙箱受限**
   - 影响: 无法限制内存和CPU
   - 解决方案: 添加警告，建议使用WSL2

### 中优先级

4. **颜色输出在Windows CMD中显示异常**
   - 影响: 终端输出可能有乱码
   - 解决方案: 使用`colorama`库

5. **文件编码问题**
   - 影响: 某些文件在Windows上可能乱码
   - 解决方案: 统一使用UTF-8编码

---

## 🛠️ 修复计划

详见: [PLATFORM_FIX_PLAN.md](PLATFORM_FIX_PLAN.md)

---

**返回 [项目主页](../README.md) | [安全说明](SECURITY.md)**

