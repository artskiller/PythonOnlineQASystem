新增批量运行脚本与依赖：
- requirements.txt（根目录）：pandas 与 numpy 版本范围
- interview_exercises/run_all.py：一键运行所有套题自检，支持 --mode answers|blank|both，自动检测 pandas 缺失时跳过 B/E。