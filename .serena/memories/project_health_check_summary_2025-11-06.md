# 项目健康检查摘要（2025-11-06）

- 代码结构：清晰分层（tools / interview_exercises / web / docs / scripts），入口脚本与学习工具可用。
- CI 配置：.github/workflows/test.yml 使用 Python 3.11，运行 answers 模式，依赖通过 requirements.txt 管理。
- 依赖：根 requirements.txt（仅 B/E 题依赖 pandas/numpy），web/requirements.txt（Flask 与可选 AI 依赖）。
- 可执行性：本地环境当前无 Python 解释器，未能运行 compileall 或自检脚本；在具备 Python3 环境下按 Makefile 目标可正常运行。
- 关键脚本：
  - interview_exercises/run_all.py：按需跳过未安装 pandas 的套题（B/E/G）。
  - tools/learn.py、tools/progress.py：交互/进度工具逻辑完成度高。
  - web/app.py：提供 /api/questions、/api/question/<set_id>、/api/run 端点；/api/run 存在代码执行风险，需仅用于受控本地环境。
- 发现问题/风险：
  1) 大量 _blank.py 含 TODO，为训练设计，非缺陷；默认 CI 仅跑 answers，安全。
  2) web 前端依赖外部 CDN（CodeMirror），离线环境需本地化静态资源。
  3) /api/run 执行任意代码（30s 超时，缺少资源/权限隔离），不宜对外开放。
  4) scripts/organize_exercises.sh 使用符号链接，Windows/部分 FS 可能不兼容。
- 建议改进：
  - 提供本地化前端依赖包或构建产物，避免 CDN 依赖。
  - /api/run 在生产或共享环境使用容器/沙箱（非 root 用户、cgroup/rlimit、seccomp）。
  - 可补充 pyproject.toml/ruff 配置以统一风格检查（可选）。
