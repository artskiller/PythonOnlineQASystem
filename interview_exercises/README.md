# Python 面试练习套题（AI 工程师 / 税务方向）

[![CI](https://github.com/OWNER/REPO/actions/workflows/test.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/test.yml)

> 将上方徽章中的 `OWNER/REPO` 替换为你的 GitHub 仓库路径。

本目录包含 5 套 Python 代码填空题（每套含空白版与答案版），覆盖基础语法、pandas 数据处理、算法与 Pythonic、并发与性能、业务综合（个税/增值税/发票/报表）。运行每个 `.py` 文件会自动执行自检断言，全部通过即代表该套题完成。

---

## 目录结构
- 基础与标准库：`set_A_blank.py`、`set_A_answers.py`
- pandas 数据处理：`set_B_blank.py`、`set_B_answers.py`
- 算法与 Pythonic：`set_C_blank.py`、`set_C_answers.py`
- 并发与性能：`set_D_blank.py`、`set_D_answers.py`
- 业务综合：`set_E_blank.py`、`set_E_answers.py`
- 文本与高精度：`set_F_blank.py`、`set_F_answers.py`
- pandas 进阶：`set_G_blank.py`、`set_G_answers.py`
- 并发进阶：`set_H_blank.py`、`set_H_answers.py`
- 算法进阶：`set_I_blank.py`、`set_I_answers.py`
- 业务进阶：`set_J_blank.py`、`set_J_answers.py`
- 基础综合（混合题型）：`set_K_blank.py`、`set_K_answers.py`
- 调试与修复：`set_L_blank.py`、`set_L_answers.py`
- 设计与文档：`set_M_blank.py`、`set_M_answers.py`
- 异常与上下文：`set_N_blank.py`、`set_N_answers.py`
- 算法与实战：`set_O_blank.py`、`set_O_answers.py`
- 日志与可观测性：`set_P_blank.py`、`set_P_answers.py`
- 脱敏与合规：`set_Q_blank.py`、`set_Q_answers.py`
- SQLite 与 SQL 安全：`set_R_blank.py`、`set_R_answers.py`
- API 契约（纯标准库）：`set_S_blank.py`、`set_S_answers.py`
- 异步编排：`set_T_blank.py`、`set_T_answers.py`
- Tracing 模拟：`set_U_blank.py`、`set_U_answers.py`
- OCR 文本清洗：`set_V_blank.py`、`set_V_answers.py`
- 批量导入流水线：`set_W_blank.py`、`set_W_answers.py`
- 审计日志轮转：`set_X_blank.py`、`set_X_answers.py`
- 简易规则引擎：`set_Y_blank.py`、`set_Y_answers.py`
- 端到端小项目：`set_Z_blank.py`、`set_Z_answers.py`
- 端到端·并发版：`set_AA_blank.py`、`set_AA_answers.py`
- 端到端·HTTP 服务版：`set_AB_blank.py`、`set_AB_answers.py`

注：每个答案文件均额外生成了“注解版”，文件名为 `*_answers_annotated.py`，在需要填写的关键位置之前加入了中文注释，说明解题思路与答案来由，便于复习与面试讲解。

另附：
- 全部题目“手工精讲”汇总（Why vs How / 复杂度 / 边界等）：`ALL_DEEP_DIVE.md`
- 题库（题面版）：`QUESTION_BANK.md`
- 题库（答案与评分要点版）：`QUESTION_BANK_WITH_SOLUTIONS.md`
- 题库（题面+答案折叠版，支持展开/收起）：`QUESTION_BANK_COMBINED.md`
- 分岗组卷：
  - 数据工程岗：`EXAM_DATA.md`
  - 平台工程岗：`EXAM_PLATFORM.md`
  - 应用工程岗：`EXAM_APP.md`

---

## 覆盖知识点
- A 基础与标准库：正则提取、字典/集合推导、多键排序、生成器、上下文管理器、CSV 读写
- B pandas：读取与合并、groupby 聚合、merge 匹配、向量化计算、月末与 period、正则列提取
- C 算法与 Pythonic：LRU（OrderedDict）、TopK（heapq）、yield from、二分、itertools.groupby、dataclass 排序
- D 并发与性能：线程池、asyncio.gather、numpy 向量化、流式分块生成器、去重保序、logging 配置
- E 业务综合：个税速算、增值税销项/进项、发票文本解析与校验、账号脱敏、月度报表透视
- F 文本与高精度：Decimal 舍入、正则多行、上下文管理、金额格式化、键聚合、税号校验
- G pandas 进阶：CSV 类型解析、分类类型、环比/同比、滚动平均、透视合计、时区转换
- H 并发进阶：asyncio 限流、线程安全计数器、指数退避重试、生产者-消费者
- I 算法进阶：Trie 脱敏、并查集、KMP、滑窗、快速选择、拓扑排序
- J 业务进阶：发票近似去重、JSONL 过滤、税率标签、CSV 汇总、信用代码简校验、舍入对比
- K 基础综合：选择/判断/实现/输出预测/小脚本
- L 调试与修复：字典合并、路径拼接、分块、日志配置
- M 设计与文档：交易 dataclass、聚合、协议选择、文档生成
- N 异常与上下文：文件写入上下文、重试装饰器、try/else/finally 语义
- O 算法与实战：网格最短路、日志解析、令牌化、JSON 分组
- P 日志与可观测性：JSON 结构化日志、采样过滤、耗时统计、上下文注入
- Q 脱敏与合规：哈希+盐、姓名/邮箱脱敏、k-匿名、身份证格式检测
- R SQLite 与 SQL 安全：参数化插入/查询、主键冲突处理、左连接汇总
- S API 契约：路由分发、参数与 JSON 校验、错误码与消息
- T 异步编排：去重、背压、重试退避与抖动、优雅关闭
- U Tracing 模拟：trace/span 上下文、事件输出 JSON
- V OCR 文本清洗：规范化与字段抽取（代码/号码/金额）
- W 批量导入流水线：校验→事务落库→回执
- X 审计日志轮转：按大小轮转与备份
- Y 简易规则引擎：条件匹配与动作执行（税额计算）
- Z 端到端小项目：CLI→校验→转换→持久化→报表→JSON 日志
- AA 端到端·并发版：批量扫描→并发解析（隔离+重试）→集中落库→汇总报表
- AB 端到端·HTTP 服务：POST /report 接口→校验→聚合返回JSON报表，含 /shutdown 测试端点

---

## 运行环境
- Python 3.8+（推荐 3.10 或更高）
- 仅 B/E/G 套题依赖第三方包：`pandas`（可选 `numpy`）

可选：使用虚拟环境隔离依赖
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
```

---

## 安装依赖（仅 B/E 必需）
```bash
pip install pandas numpy
```

> 说明：B 套题中与 Excel 相关的自检通过“打桩”方式模拟 `pd.read_excel`，无需实际 Excel 文件或引擎。

---

## 快速上手（venv 推荐）
```bash
# 1) 创建并启用本地虚拟环境
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 2) 升级 pip 并安装依赖（B/E/G 需要）
python -m pip install -U pip
pip install -r requirements.txt

# 3) 一键验证所有答案版题目
python interview_exercises/run_all.py --mode answers

# 完成后退出环境（可选）
deactivate
```

> 提示：若只练习标准库题目（不含 B/E/G），可跳过安装 requirements；需要 pandas 时再安装即可。

---

## 快速运行
- 做题（空白版，自行填写 `____` 后运行自检）：
```bash
python interview_exercises/set_A_blank.py
```
- 查看/对照答案（答案版，含完整实现）：
```bash
python interview_exercises/set_A_answers.py
```
- 其他套题将 `A` 替换为 `B/C/D/E` 即可。

### 一键运行所有自检
- 运行答案版（默认，验证环境与逻辑）：
```bash
python interview_exercises/run_all.py --mode answers
```
- 运行空白版（未填写将失败，适合练习后自检）：
```bash
python interview_exercises/run_all.py --mode blank
```
- 先空白后答案：
```bash
python interview_exercises/run_all.py --mode both
```
> 提示：若未安装 `pandas`，脚本会自动跳过 B/E/G 套题。

### Makefile 与脚本快捷方式
- 使用 Make：
```bash
make install       # 安装 pandas/numpy（仅 B/E 需要）
make answers       # 运行答案版
make blank         # 运行空白版
make both          # 先空白后答案
# 或自定义模式
make run MODE=blank
```
- 使用 bash 脚本：
```bash
bash scripts/run_all.sh answers
bash scripts/run_all.sh blank
bash scripts/run_all.sh both
```

### 压测并发版（AA）
```bash
python interview_exercises/bench_AA.py --files 200 --rows 5 --workers 8
```
输出示例：`files=200 rows=1000 workers=8 time=0.85s throughput=1176.5 rows/s`

---

## 推荐做题顺序与时间（120 分钟建议）
1. A 基础热身（15 分钟）
2. B pandas（35 分钟）
3. E 业务综合（35 分钟）
4. C 算法与 Pythonic（20 分钟）
5. 机动/查漏补缺（15 分钟）

策略：
- 优先保证“能跑通”的 5 题，通过断言后再做优化。
- 统一风格：中文注释、类型注解、边界处理（空数据/非法输入）。
- pandas 侧重向量化；合并后立即处理缺失值与类型一致性。

---

## 自检与评分建议
- 运行空白版文件：所有断言通过视为该题完成。
- 若仅部分通过：先根据断言失败信息定位修改，再最小化变更修复。
- 需要参考答案时：运行对应 `*_answers.py` 并对照差异点复盘。

---

## 常见问题（FAQ）
- Q: 没有安装 pandas/numpy 怎么办？
  - A: 仅 B/E 需要；可跳过或先安装 `pip install pandas numpy`。
- Q: Excel 相关会报引擎错误吗？
  - A: 自检使用函数打桩，不依赖实际 Excel 引擎，不会报错。
- Q: Windows 路径与编码问题？
  - A: 使用 `utf-8`，路径请用原样命令；如有中文路径建议在终端使用 UTF-8。

---

## 版权与使用
- 仅用于个人学习与面试训练；请勿用于商业用途或外传泄露。

祝顺利上岸！

---

## CI 集成（GitHub Actions）
- 工作流：`.github/workflows/test.yml`
- 触发：`push` / `pull_request` / `workflow_dispatch`
- 动作：
  - 安装依赖（`requirements.txt`）
  - 执行：`python interview_exercises/run_all.py --mode answers`
  - 使用 pip 缓存加速安装

如需本地模拟 CI：
```bash
make install
make answers
```
