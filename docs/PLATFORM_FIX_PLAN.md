# 🔧 跨平台兼容性修复方案

本文档详细说明如何修复pythonLearn项目在不同平台上的兼容性问题。

---

## 📋 修复清单

### ✅ 已完成

- [x] 平台检测（`sys.platform`）
- [x] 资源限制兼容性（`web/security/sandbox.py`）
- [x] 信号处理兼容性（`web/security/sandbox.py`）
- [x] 路径处理（使用`pathlib.Path`）

### 🔄 进行中

- [ ] 创建跨平台启动脚本
- [ ] Shell脚本转Python
- [ ] Windows特定文档
- [ ] 颜色输出兼容性

### 📅 计划中

- [ ] 自动化测试（多平台CI/CD）
- [ ] Docker镜像优化
- [ ] 性能优化

---

## 🎯 修复方案

### 1. 创建跨平台启动脚本

#### 问题
- Makefile在Windows上不可用
- Shell脚本在Windows CMD中无法运行

#### 解决方案
创建`setup.py`作为跨平台入口

**文件**: `setup.py`

```python
#!/usr/bin/env python3
"""
跨平台项目管理脚本
替代Makefile，支持Windows/macOS/Linux
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class ProjectManager:
    def __init__(self):
        self.root = Path(__file__).parent
        self.venv = self.root / '.venv'
        self.python = self._get_python()
    
    def _get_python(self):
        """获取Python可执行文件路径"""
        if sys.platform == 'win32':
            return self.venv / 'Scripts' / 'python.exe'
        else:
            return self.venv / 'bin' / 'python'
    
    def setup(self):
        """初始化项目"""
        print("🔧 初始化项目...")
        
        # 创建虚拟环境
        if not self.venv.exists():
            print("📦 创建虚拟环境...")
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv)])
        
        # 安装依赖
        print("📥 安装依赖...")
        pip = self.venv / ('Scripts' if sys.platform == 'win32' else 'bin') / 'pip'
        subprocess.run([str(pip), 'install', '-U', 'pip'])
        subprocess.run([str(pip), 'install', '-r', 'requirements.txt'])
        
        # 组织文件
        print("📁 组织练习文件...")
        self.organize()
        
        print("\n✅ 项目初始化完成！")
    
    def organize(self):
        """组织练习文件（Python实现）"""
        # TODO: 实现organize_exercises.sh的Python版本
        pass
    
    def web(self):
        """启动Web平台"""
        print("🌐 启动Web学习平台...")
        print("📖 访问地址: http://localhost:8080")
        print("💡 按 Ctrl+C 停止服务\n")
        
        # 安装Web依赖
        pip = self.venv / ('Scripts' if sys.platform == 'win32' else 'bin') / 'pip'
        subprocess.run([str(pip), 'install', '-r', 'web/requirements.txt'])
        
        # 启动应用
        os.chdir(self.root / 'web')
        subprocess.run([str(self.python), 'app.py'])
    
    def learn(self, level='01'):
        """启动交互式学习"""
        subprocess.run([str(self.python), 'tools/learn.py', '--level', level])
    
    def progress(self):
        """查看学习进度"""
        subprocess.run([str(self.python), 'tools/progress.py', '--show'])
    
    def test(self):
        """运行测试"""
        subprocess.run([str(self.python), 'web/tests/test_security.py'])
    
    def clean(self):
        """清理临时文件"""
        print("🧹 清理临时文件...")
        
        # 清理__pycache__
        for pycache in self.root.rglob('__pycache__'):
            import shutil
            shutil.rmtree(pycache, ignore_errors=True)
        
        # 清理.pyc文件
        for pyc in self.root.rglob('*.pyc'):
            pyc.unlink(missing_ok=True)
        
        print("✅ 清理完成！")

def main():
    parser = argparse.ArgumentParser(description='pythonLearn 项目管理')
    parser.add_argument('command', choices=[
        'setup', 'web', 'learn', 'progress', 'test', 'clean'
    ], help='要执行的命令')
    parser.add_argument('--level', default='01', help='学习阶段（用于learn命令）')
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    
    if args.command == 'setup':
        manager.setup()
    elif args.command == 'web':
        manager.web()
    elif args.command == 'learn':
        manager.learn(args.level)
    elif args.command == 'progress':
        manager.progress()
    elif args.command == 'test':
        manager.test()
    elif args.command == 'clean':
        manager.clean()

if __name__ == '__main__':
    main()
```

**使用方式**:
```bash
# 所有平台通用
python setup.py setup      # 初始化项目
python setup.py web        # 启动Web平台
python setup.py learn --level 01  # 开始学习
python setup.py progress   # 查看进度
python setup.py test       # 运行测试
python setup.py clean      # 清理文件
```

---

### 2. Shell脚本转Python

#### 问题
`scripts/organize_exercises.sh`在Windows上无法运行

#### 解决方案
创建`scripts/organize_exercises.py`

**文件**: `scripts/organize_exercises.py`

```python
#!/usr/bin/env python3
"""
组织练习文件脚本（Python版本）
跨平台兼容
"""

import os
import shutil
from pathlib import Path

def organize_exercises():
    """组织练习文件到分级目录"""
    root = Path(__file__).parent.parent
    exercises_dir = root / 'interview_exercises'
    
    if not exercises_dir.exists():
        print("❌ interview_exercises目录不存在")
        return
    
    print("📁 组织练习文件...")
    
    # 创建分级目录
    levels = {
        '01_基础': ['A', 'B', 'C', 'D', 'E'],
        '02_进阶': ['F', 'G', 'H', 'I', 'J'],
        # ... 其他级别
    }
    
    for level_name, sets in levels.items():
        level_dir = exercises_dir / level_name
        level_dir.mkdir(exist_ok=True)
        
        for set_name in sets:
            # 移动文件
            for suffix in ['_answers.py', '_blank.py', '_test.py']:
                src = exercises_dir / f'set_{set_name}{suffix}'
                if src.exists():
                    dst = level_dir / src.name
                    shutil.move(str(src), str(dst))
    
    print("✅ 文件组织完成！")

if __name__ == '__main__':
    organize_exercises()
```

---

### 3. 增强安全沙箱的Windows支持

#### 问题
Windows上无法使用`resource`模块限制资源

#### 解决方案
添加Windows特定的警告和文档

**文件**: `web/security/sandbox.py`（已修改）

添加Windows检测和警告:

```python
def __init__(self):
    self.violations = []
    
    # Windows平台警告
    if sys.platform == 'win32':
        import warnings
        warnings.warn(
            "Windows平台不支持完整的资源限制。"
            "建议使用WSL2或Linux环境以获得完整的安全保护。",
            RuntimeWarning
        )
```

---

### 4. 颜色输出兼容性

#### 问题
Windows CMD不支持ANSI颜色代码

#### 解决方案
使用`colorama`库

**修改**: `web/test_web_security.sh` → `web/test_web_security.py`

```python
#!/usr/bin/env python3
"""
Web应用安全测试脚本（Python版本）
跨平台兼容
"""

import sys
import requests

# Windows颜色支持
if sys.platform == 'win32':
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def test_dangerous_code():
    """测试危险代码被阻止"""
    print("2️⃣  测试危险代码被阻止...")
    
    tests = [
        ("import os", "import os"),
        ("eval()", 'eval("1+1")'),
        ("open()", 'open("/etc/passwd")'),
    ]
    
    for name, code in tests:
        response = requests.post(
            'http://localhost:8080/api/run',
            json={'code': code}
        )
        result = response.json()
        
        if not result.get('success'):
            print(f"   测试: {name} ... {Colors.GREEN}✅ 被阻止{Colors.NC}")
        else:
            print(f"   测试: {name} ... {Colors.RED}❌ 未被阻止！{Colors.NC}")

if __name__ == '__main__':
    test_dangerous_code()
```

---

## 📦 依赖更新

添加到`requirements.txt`:

```
colorama>=0.4.6; sys_platform == 'win32'
```

---

## 🧪 测试计划

### 测试矩阵

| 平台 | Python版本 | 测试项 |
|------|-----------|--------|
| Ubuntu 22.04 | 3.9, 3.10, 3.11 | 全部 |
| macOS 13 | 3.9, 3.10, 3.11 | 全部 |
| Windows 11 | 3.9, 3.10, 3.11 | 核心功能 |
| WSL2 Ubuntu | 3.9, 3.10, 3.11 | 全部 |

### 测试命令

```bash
# Linux/macOS
make test

# Windows
python setup.py test
```

---

**下一步**: 实施修复方案

**返回 [兼容性指南](PLATFORM_COMPATIBILITY.md) | [项目主页](../README.md)**

