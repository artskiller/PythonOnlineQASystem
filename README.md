# Python 面试练习套题

[![CI](https://github.com/OWNER/REPO/actions/workflows/test.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/test.yml)

> 注意：当前项目不是 Git 仓库或未配置远程。将上述徽章中的 `OWNER/REPO` 替换为你的 GitHub 仓库路径（例如 `yourname/pythonLearn`）。

- 练习题与说明：见 `interview_exercises/README.md`
- 一键运行：`python interview_exercises/run_all.py --mode answers`
- Makefile：`make answers`（先 `make install` 安装依赖）

## 快速上手（venv 推荐）
```bash
# 在项目根目录：创建并启用虚拟环境
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 升级 pip 并安装依赖（B/E/G 需要 pandas/numpy）
python -m pip install -U pip
pip install -r requirements.txt

# 一键验证（答案版）
python interview_exercises/run_all.py --mode answers

# 完成后退出环境（可选）
deactivate
```
