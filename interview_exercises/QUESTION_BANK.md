# 税务师事务所·AI 工程师 面试题库（新格式·Markdown）

说明
- 题库覆盖：Python 基础/进阶、数据处理（pandas/NumPy）、并发/异步、日志与可观测性、SQL/SQLite、API 设计、数据合规、财税业务（增值税/个税/发票）与端到端工程实践
- 组织形式参考主流在线面经与题库格式：分题型、给出清晰的题干模板（题面/要求/约束/示例/考察点/用时建议）
- 适配 120–150 分钟面试机试或 2 小时在线笔试，可按板块抽取组卷

评分建议（可选）
- 单选/多选/判断：每题 1–2 分；简答/改错：每题 3–5 分；编程/SQL/系统设计/业务综合：每题 5–12 分
- 通过线可设为 60/100 或 75/120，按岗位等级微调

---

## A. 单选题（12 题，每题 1 分）

A1. 下列关于 Python 字典（dict）的说法，正确的是（ ）。
- A. 键（key）可重复，后插入的覆盖前一个
- B. 平均情况下按键查找时间复杂度为 O(1)
- C. Python3.7+ 中 dict 遍历顺序是随机的
- D. dict 的键必须是字符串
- 要求：选择 1 项
- 考察点：哈希表、时空复杂度、实现细节
- 建议用时：1 分钟

A2. 下列正则用于匹配“整数或小数”的更鲁棒写法是（ ）。
- A. `\d+\.\d+?`
- B. `\d+(\.\d+)?`
- C. `(?:\d+|\d+\.\d+)`
- D. `\d*\.\d*`
- 要求：选择 1 项；考虑贪婪/惰性、可选小数部分
- 考察点：正则分组/非捕获组
- 建议用时：1 分钟

A3. 关于 `sorted(xs, key=lambda x: (x.date, -x.amount))` 的说法，正确的是（ ）。
- A. 先按 `amount` 升序，再按 `date` 降序
- B. 先按 `date` 升序，同日内按 `amount` 降序
- C. 仅按 `amount` 排序
- D. 表达式非法，不能在 key 中取负号
- 考察点：排序键与降序技巧

A4. 下列关于协程并发的描述，正确的是（ ）。
- A. `asyncio.gather` 会顺序执行协程
- B. `await asyncio.sleep(0)` 等效阻塞当前线程
- C. `asyncio.Semaphore` 可用于限流
- D. 协程天然适合 CPU 密集任务

A5. pandas 中计算环比同比常用的方法是（ ）。
- A. `Series.diff(12)`
- B. `Series.pct_change(1)` 与 `Series.pct_change(12)`
- C. `Series.shift(12).pct_change()`
- D. `Series.rolling(12).sum()`

A6. `sqlite3` 参数化查询中占位符用法正确的是（ ）。
- A. `SELECT * FROM t WHERE id = :1`
- B. `SELECT * FROM t WHERE id = %s`
- C. `SELECT * FROM t WHERE id = ?`
- D. `SELECT * FROM t WHERE id = $1`

A7. 关于日志配置与输出，推荐做法是（ ）。
- A. 多次调用 `basicConfig` 即可修改现有 Handler 格式
- B. 统一输出单行 JSON 便于搜索分析
- C. 将异常信息直接 `print` 到控制台
- D. 在生产环境关闭 INFO 日志

A8. LRU 缓存用 `OrderedDict` 实现时，淘汰最旧元素的正确写法是（ ）。
- A. `popitem(True)`  
- B. `popitem(False)`  
- C. `pop(0)`  
- D. `pop(-1)`

A9. 关于 `@contextmanager` 的说法，正确的是（ ）。
- A. `yield` 前后分别对应 `__enter__/__exit__`
- B. 发生异常时不会执行 `finally`
- C. 仅能用于文件对象
- D. 进入与退出与 `with` 无关

A10. JSON Lines（每行一个 JSON）读取时，更合适的是（ ）。
- A. 一次性读入内存后 `json.loads` 解析
- B. 行流式读取，逐行 `json.loads`
- C. 使用 `eval`
- D. 使用 `ast.literal_eval`

A11. 税额拆分（含税→不含税+税额）常用公式是（ ）。
- A. `net = amount * (1 - rate)`，`tax = amount - net`
- B. `net = amount / (1 + rate)`，`tax = amount - net`
- C. `tax = amount * rate`
- D. `net = amount - rate`

A12. pandas 计算月末常用写法是（ ）。
- A. `date + MonthBegin(0)`
- B. `date + MonthEnd(0)`
- C. `date + MonthEnd(1)` 必须用 1
- D. `date.replace(day=31)`

---

## B. 多选题（6 题，每题 2 分）

B1. 关于 `asyncio` 并发最佳实践，哪些是正确的（ ）。
- A. 使用 `Semaphore` 控制外部 API 调用并发度
- B. 阻塞 I/O 建议直接 `await` 同步函数
- C. 将 CPU 密集任务 offload 至 `run_in_executor`
- D. `gather` 返回的顺序与传入顺序一致
- 选择 2–3 项

B2. 数据合规与脱敏，哪些做法合理（ ）。
- A. 账号脱敏仅保留后 4 位，其余 `*` 代替
- B. 税号只要长度为 18 即可判定合法
- C. 姓名与邮箱脱敏，保留必要最小信息
- D. 哈希+盐替代可逆加密存储敏感标识

B3. pandas 合并与聚合中，哪些易错点需要重点规避（ ）。
- A. 键的 dtype 不一致
- B. `groupby` 后列名冲突
- C. `merge` 后缺失值未处理
- D. 时间列未标准化为同一时区

B4. 结构化日志实践中，建议包含哪些字段（ ）。
- A. `ts`（时间戳，秒或毫秒）
- B. `level`（级别）
- C. `trace_id/span_id`（请求链路）
- D. `msg` 与业务字段（如 file, rows）

B5. SQL 参数化写法规范（ ）。
- A. `... WHERE id = ?`，参数用元组传入
- B. `... WHERE id = %s`，可跨方言通用
- C. `... WHERE id = :id`，sqlite3 中与 `?` 等效
- D. `... WHERE id = ?`，避免字符串拼接

B6. 大文件处理时的稳健做法（ ）。
- A. 分块流式处理
- B. 生成器 + `yield from` 解耦逻辑
- C. 全量读取进内存加速吞吐
- D. 异常/坏行隔离并记录

---

## C. 判断题（6 题，每题 1 分）

C1. Python 中 list 的 `append` 平均复杂度为 O(1)。  对/错

C2. `logging.basicConfig` 可多次调用覆盖旧 Handler 的格式。 对/错

C3. pandas `pct_change(12)` 适用于同比计算（以 12 期为周期）。 对/错

C4. SQLite 参数化查询可直接写为 `... WHERE id = $1`。 对/错

C5. 协程非常适合 CPU 密集场景。 对/错

C6. `OrderedDict.popitem(False)` 弹出的是最新插入项。 对/错

---

## D. 简答题（6 题，每题 4 分）

D1. 简述在生产系统中采用“单行 JSON 日志”的优势与注意事项。
- 要点：可观测性、检索性、字段标准化、时区/时精度、异常结构化

D2. 说明 `contextvars` 在链路追踪（trace/span）中的作用与典型用法。

D3. 比较 Decimal 与 float 在金融场景中的优缺点，并给出舍入策略推荐。

D4. 结合示例，说明 pandas `merge` 后为何要立即处理缺失值与 dtype。

D5. 说明“个税速算扣除”的基本计算思路与实现注意点（边界）。

D6. 简述“重试与退避”的设计原则（最大次数、抖动、幂等、超时）。

---

## E. 代码阅读与改错（5 题，每题 5 分）

E1. 分块生成器（找出问题并修正）
```python
buf = []
for ln in lines:
    buf.append(ln)
    if len(buf) >= n:
        yield buf
        buf.clear()  # 问题：返回对象被清空
# 修正：yield buf; buf = []
```
- 要求：指出问题与原因，给出修正方案

E2. LRU 容量策略（找错并改正）
```python
if len(d) >= cap:
    d.popitem(True)  # 问题：应该淘汰最旧元素 last=False
```

E3. 日志配置失效（找错并改正）
```python
logging.basicConfig(level=logging.DEBUG, format='%(message)s')  # 级别/格式不达标
```
- 要求：给出 INFO+时间/级别/消息的配置方案

E4. pandas 月末计算错误（找错并改正）
```python
df['month_end'] = df['date'] + pd.offsets.Day(31)  # 不正确
```
- 正确：`MonthEnd(0)`

E5. SQL 注入风险（找错并改正）
```python
sql = f"SELECT * FROM t WHERE code='{code}'"  # 字符串拼接
```
- 正确：参数化 `WHERE code = ?`

---

## F. 编程题（8 题，每题 8–10 分）

F1. 金额提取与清洗（正则）
- 题面：给定字符串，提取所有“整数或小数”金额，返回浮点列表
- 函数签名：`def extract_amounts(text: str) -> List[float]: ...`
- 约束：O(n)；支持中文标点；保序
- 示例："合计: 123, 税额: 45.67 元" → `[123.0, 45.67]`
- 考察点：正则、边界处理

F2. 部门汇总（字典/推导）
- 输入：`List[Tuple[str, float]]`（部门, 金额）
- 输出：`Dict[str, float]`（求和）
- 约束：O(n)；稳定；浮点舍入 2 位

F3. 多键排序：日期升序/金额降序
- 输入：`List[Dict]`，字段 `date: YYYY-MM-DD`，`amount: float`
- 输出：排序后的列表
- 约束：O(n log n)

F4. CSV 读取并新增税额列
- 输入：CSV 文本，包含 `amount` 列；参数 `rate`
- 输出：新增 `tax` 列的 CSV 文本
- 约束：四舍五入两位；保留表头

F5. pandas：向量化拆分含税金额
- 输入：`DataFrame` 有列 `amount`
- 输出：新增 `net`/`tax` 列
- 约束：`np.round(..., 2)`；避免 `apply`

F6. 并发限流抓取（asyncio）
- 题面：给定整数列表，使用协程并发+信号量限流，返回每个元素+1 的结果列表
- 要求：`asyncio.gather` 收集；`Semaphore(limit)` 限制并发

F7. 规则引擎（条件+动作）
- 题面：实现 `match/ apply_actions/ apply_rules`，支持 `eq/ne/gt/gte/lt/lte/in` 与动作 `set/compute_tax`
- 输入：规则列表与行对象
- 输出：作用后的行对象

F8. 网格最短路（BFS）
- 题面：0/1 矩阵，起点到终点的最短步数（4 邻接，1 为障碍）
- 约束：不可达返回 -1；O(n)

---

## G. SQL 题（5 题，每题 6–8 分）

公共表结构（SQLite）
```sql
CREATE TABLE invoices(
  code TEXT, number TEXT, amount REAL, rate REAL,
  date TEXT, dept TEXT, PRIMARY KEY(code, number)
);
CREATE TABLE org(
  code TEXT, number TEXT, dept TEXT
);
```

G1. 写出“左连接 org，按部门汇总含税金额总和，NULL 记为 'UNK'，结果按部门字典序”的 SQL。

G2. 写出“查询 2024-03 期间的发票总额（以 date 月份判断）”的 SQL。

G3. 写出“按 `period=YYYY-MM` 与 `dept` 汇总 `amount_sum`、`tax_sum`（税额按含税→不含税公式拆分）”的 SQL。

G4. 写出“存在于 invoices 但不在 org 中的发票清单”的 SQL。

G5. 写出“去重统计：相同 (code, number) 保留一条”的 SQL（可用窗口或聚合）。

---

## H. 系统/API 设计（4 题，每题 8–10 分）

H1. 设计 `POST /report` 接口，接收 JSON 批量发票，返回 period/dept 汇总。请给出：
- 请求/响应示例、参数校验（金额非负/税率集合/日期范围）、错误码与错误消息、幂等/去重策略、日志字段（trace_id/span_id）

H2. 设计“结构化日志规范”，至少包含字段、时间格式与时区、级别规范、异常结构化要求、采样策略与脱敏策略。

H3. 设计“并发导入流水线”：扫描→解析→校验→落库→回执。说明：背压/重试/隔离策略、幂等（主键/去重）、吞吐与一致性的权衡。

H4. 设计“税务票据 OCR 清洗与字段校验”流程：文本规范化、字段提取、校验（税号/金额/日期）、异常行隔离与报错汇总。

---

## I. 财税业务综合（6 题，每题 8–12 分）

I1. 个税速算（简化）：给定“应纳税所得额”，输出税额，写出计算逻辑、边界与单元测试要点。

I2. 增值税（销项-进项）净应纳税额：给定发票列表（含 `type`, `amount`, `rate`），计算净额并说明含税→不含税→税额的换算关系。

I3. 发票文本解析：给定多行文本，提取发票号/税号/金额，输出结构化对象。说明正则设计要点与抗噪声策略。

I4. 账号脱敏：给定文本，脱敏连续 10~19 位数字，保留末 4 位。说明合规与可逆性要求。

I5. 期间报表：按月份与部门汇总金额，输出透视表；说明缺失填充与列序控制策略。

I6. 数据质量规则：给定“规则 DSL”（如 `amount>=0`, `rate in {0.13,0.09,0.06,0.03}`），校验 CSV 并输出错误回执（行号/字段/原因）。

---

## 组卷与时间建议
- 机试（120 分钟）参考：
  - 单选×10（10 分）+ 多选×6（12 分）+ 判断×6（6 分）
  - 简答×4（16 分）+ 改错×4（20 分）
  - 编程×3（36 分）+ SQL×2（20 分）
  - 合计约 120 分
- 面试白板（60–90 分钟）参考：
  - 简答/系统设计/业务综合，按岗位等级与经历挑选 6–10 题

---

附注
- 本题库为“题面版”，不含参考答案。如需“答案版（含思路/代码/SQL/评分要点）”，可在同目录生成 `QUESTION_BANK_WITH_SOLUTIONS.md`。
- 所有题目的可运行原题与自检示例可参考 `interview_exercises` 下的各套题（A–Z，AA/AB/T 等）。
