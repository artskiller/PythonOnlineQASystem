#!/usr/bin/env python3
"""
pythonLearn 跨平台项目管理脚本
替代Makefile，支持Windows/macOS/Linux

使用方式:
    python setup.py setup      # 初始化项目
    python setup.py web        # 启动Web平台
    python setup.py learn      # 开始学习
    python setup.py progress   # 查看进度
    python setup.py test       # 运行测试
    python setup.py clean      # 清理文件
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path


class ProjectManager:
    """项目管理器"""
    
    def __init__(self):
        self.root = Path(__file__).parent
        self.venv = self.root / '.venv'
        self.python = self._get_python()
        self.pip = self._get_pip()
    
    def _get_python(self):
        """获取Python可执行文件路径"""
        if self.venv.exists():
            if sys.platform == 'win32':
                return self.venv / 'Scripts' / 'python.exe'
            else:
                return self.venv / 'bin' / 'python'
        return sys.executable
    
    def _get_pip(self):
        """获取pip可执行文件路径"""
        if self.venv.exists():
            if sys.platform == 'win32':
                return self.venv / 'Scripts' / 'pip.exe'
            else:
                return self.venv / 'bin' / 'pip'
        return 'pip'
    
    def setup(self):
        """初始化项目"""
        print("🔧 初始化项目...")
        print(f"📍 项目路径: {self.root}")
        print(f"🐍 Python版本: {sys.version.split()[0]}")
        print(f"💻 操作系统: {sys.platform}")
        print()
        
        # 创建虚拟环境
        if not self.venv.exists():
            print("📦 创建虚拟环境...")
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv)], check=True)
            print("✅ 虚拟环境创建完成")
        else:
            print("✅ 虚拟环境已存在")
        
        # 更新pip
        print("\n📥 更新pip...")
        subprocess.run([str(self.pip), 'install', '-U', 'pip'], check=True)
        
        # 安装依赖
        print("\n📥 安装项目依赖...")
        subprocess.run([str(self.pip), 'install', '-r', 'requirements.txt'], check=True)
        
        # 组织文件
        print("\n📁 组织练习文件...")
        self.organize()
        
        print("\n" + "="*60)
        print("✅ 项目初始化完成！")
        print("="*60)
        print("\n💡 下一步:")
        if sys.platform == 'win32':
            print("  1. 激活虚拟环境: .venv\\Scripts\\activate")
        else:
            print("  1. 激活虚拟环境: source .venv/bin/activate")
        print("  2. 启动Web平台: python setup.py web")
        print("  3. 或开始学习: python setup.py learn")
        print()
    
    def organize(self):
        """组织练习文件"""
        # 简单实现：确保目录存在
        exercises_dir = self.root / 'interview_exercises'
        if exercises_dir.exists():
            print("✅ 练习文件目录已存在")
        else:
            print("⚠️  练习文件目录不存在")
    
    def web(self):
        """启动Web平台"""
        print("🌐 启动Web学习平台...")
        print("="*60)
        
        # 安装Web依赖
        print("📦 检查Web依赖...")
        web_req = self.root / 'web' / 'requirements.txt'
        if web_req.exists():
            subprocess.run([str(self.pip), 'install', '-r', str(web_req)], check=True)
        
        print("\n📖 访问地址: http://localhost:8080")
        print("💡 按 Ctrl+C 停止服务")
        print("="*60)
        print()
        
        # 启动应用
        web_dir = self.root / 'web'
        app_file = web_dir / 'app.py'
        
        if not app_file.exists():
            print("❌ 错误: web/app.py 不存在")
            return
        
        # 切换到web目录并运行
        os.chdir(web_dir)
        subprocess.run([str(self.python), 'app.py'])
    
    def learn(self, level='01'):
        """启动交互式学习"""
        learn_script = self.root / 'tools' / 'learn.py'
        if not learn_script.exists():
            print("❌ 错误: tools/learn.py 不存在")
            return
        
        subprocess.run([str(self.python), str(learn_script), '--level', level])
    
    def progress(self):
        """查看学习进度"""
        progress_script = self.root / 'tools' / 'progress.py'
        if not progress_script.exists():
            print("❌ 错误: tools/progress.py 不存在")
            return
        
        subprocess.run([str(self.python), str(progress_script), '--show'])
    
    def test(self):
        """运行安全测试"""
        print("🧪 运行安全测试...")
        test_script = self.root / 'web' / 'tests' / 'test_security.py'
        
        if not test_script.exists():
            print("❌ 错误: web/tests/test_security.py 不存在")
            return
        
        subprocess.run([str(self.python), str(test_script)])
    
    def clean(self):
        """清理临时文件"""
        print("🧹 清理临时文件...")
        
        count = 0
        
        # 清理__pycache__
        for pycache in self.root.rglob('__pycache__'):
            shutil.rmtree(pycache, ignore_errors=True)
            count += 1
        
        # 清理.pyc文件
        for pyc in self.root.rglob('*.pyc'):
            pyc.unlink(missing_ok=True)
            count += 1
        
        # 清理.egg-info
        for egg in self.root.rglob('*.egg-info'):
            shutil.rmtree(egg, ignore_errors=True)
            count += 1
        
        print(f"✅ 清理完成！删除了 {count} 个临时文件/目录")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='pythonLearn 项目管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python setup.py setup              初始化项目
  python setup.py web                启动Web平台
  python setup.py learn --level 02   学习第2阶段
  python setup.py progress           查看进度
  python setup.py test               运行测试
  python setup.py clean              清理临时文件
        """
    )
    
    parser.add_argument(
        'command',
        choices=['setup', 'web', 'learn', 'progress', 'test', 'clean'],
        help='要执行的命令'
    )
    parser.add_argument(
        '--level',
        default='01',
        help='学习阶段（用于learn命令，默认: 01）'
    )
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    
    try:
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
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

