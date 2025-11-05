# 简易 Makefile：本地/CI 快捷运行
# 使用方式：
#   make install          # 安装依赖（仅 B/E 需要）
#   make answers          # 运行答案版自检
#   make blank            # 运行空白版自检
#   make both             # 先空白后答案
#   make run MODE=blank   # 自定义模式（answers|blank|both）

SHELL := /bin/bash
PY ?= python
RUNNER := interview_exercises/run_all.py
MODE ?= answers

.PHONY: help install run answers blank both

help:
	@echo "可用目标："
	@echo "  make install          安装依赖（pandas/numpy）"
	@echo "  make answers          运行答案版自检"
	@echo "  make blank            运行空白版自检"
	@echo "  make both             先空白后答案"
	@echo "  make run MODE=blank   指定模式运行（answers|blank|both）"

install:
	$(PY) -m pip install -r requirements.txt

run:
	$(PY) $(RUNNER) --mode $(MODE)

answers:
	$(PY) $(RUNNER) --mode answers

blank:
	$(PY) $(RUNNER) --mode blank

both:
	$(PY) $(RUNNER) --mode both

