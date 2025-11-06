# Python 学习项目 Makefile
# 使用方式：
#   make setup            # 初始化项目（创建虚拟环境、安装依赖、组织文件）
#   make install          # 安装依赖
#   make learn LEVEL=01   # 启动交互式学习
#   make progress         # 查看学习进度
#   make test             # 运行所有测试
#   make clean            # 清理临时文件

SHELL := /bin/bash
PY ?= python3
VENV := .venv
RUNNER := interview_exercises/run_all.py
MODE ?= answers
LEVEL ?= 01

.PHONY: help setup install organize learn progress test answers blank both clean web web-install web-docker

help:
	@echo "🎓 Python 学习项目 - 可用命令："
	@echo ""
	@echo "  🌐 Web学习平台（推荐）："
	@echo "    make web              启动Web学习平台"
	@echo "    make web-install      安装Web依赖"
	@echo "    make web-docker       使用Docker运行Web平台"
	@echo ""
	@echo "  📦 环境设置："
	@echo "    make setup            初始化项目（推荐首次使用）"
	@echo "    make install          安装依赖（pandas/numpy）"
	@echo "    make organize         组织练习文件到分级目录"
	@echo ""
	@echo "  📚 学习工具："
	@echo "    make learn LEVEL=01   启动交互式学习（指定阶段）"
	@echo "    make progress         查看学习进度"
	@echo "    make stats            查看详细统计"
	@echo ""
	@echo "  🧪 测试运行："
	@echo "    make test             运行所有测试"
	@echo "    make answers          运行答案版自检"
	@echo "    make blank            运行空白版自检"
	@echo ""
	@echo "  🧹 清理："
	@echo "    make clean            清理临时文件"
	@echo ""
	@echo "  💡 快速开始："
	@echo "    1. make web           # Web学习平台（推荐）"
	@echo "    2. make setup         # 命令行模式"
	@echo "    3. make learn         # 开始学习"
	@echo "    4. make progress      # 查看进度"

# 初始化项目
setup:
	@echo "🔧 初始化项目..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 创建虚拟环境..."; \
		$(PY) -m venv $(VENV); \
	fi
	@echo "📥 安装依赖..."
	@$(VENV)/bin/pip install -U pip
	@$(VENV)/bin/pip install -r requirements.txt
	@echo "📁 组织练习文件..."
	@bash scripts/organize_exercises.sh
	@echo ""
	@echo "✅ 项目初始化完成！"
	@echo ""
	@echo "💡 下一步："
	@echo "  1. 激活虚拟环境：source $(VENV)/bin/activate"
	@echo "  2. 开始学习：make learn"
	@echo "  3. 查看进度：make progress"

# 安装依赖
install:
	$(PY) -m pip install -r requirements.txt

# 组织练习文件
organize:
	@bash scripts/organize_exercises.sh

# 交互式学习
learn:
	@$(PY) tools/learn.py --level $(LEVEL)

# 查看进度
progress:
	@$(PY) tools/progress.py --show

# 详细统计
stats:
	@$(PY) tools/progress.py --stats

# 运行测试
run:
	$(PY) $(RUNNER) --mode $(MODE)

test: answers

# 运行答案版
answers:
	$(PY) $(RUNNER) --mode answers

# 运行空白版
blank:
	$(PY) $(RUNNER) --mode blank

# 先空白后答案
both:
	$(PY) $(RUNNER) --mode both

# Web学习平台
web-install:
	@echo "📦 安装Web依赖..."
	@$(PY) -m pip install -r web/requirements.txt
	@echo "✅ Web依赖安装完成！"

web: web-install
	@echo "🌐 启动Web学习平台..."
	@echo "📖 访问地址: http://localhost:8080"
	@echo "💡 按 Ctrl+C 停止服务"
	@echo ""
	@cd web && $(PY) app.py

web-docker:
	@echo "🐳 使用Docker启动Web平台..."
	@cd web/docker && docker-compose up -d
	@echo "✅ Web平台已启动！"
	@echo "📖 访问地址: http://localhost:8080"

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -f .learning_progress.json
	@echo "✅ 清理完成！"
