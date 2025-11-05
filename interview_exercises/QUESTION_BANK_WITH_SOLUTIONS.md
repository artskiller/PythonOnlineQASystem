# 税务师事务所·AI 工程师 面试题库（答案与评分要点版）

说明
- 与 QUESTION_BANK.md 一一对应：给出参考答案、要点与评分建议（rubric）
- 选择/判断给出唯一或多选答案；简答/改错/编程/SQL/系统/业务给出评分要点与参考实现要点

---

## A. 单选题（每题 1 分）
- A1：B（dict 平均按键查 O(1)）
- A2：B（`\d+(?:\.\d+)?` 更简洁鲁棒；C 也可，但 B 更常用）
- A3：B（日期升序，同日金额降序，降序通过取负实现）
- A4：C（Semaphore 可限流；gather 并发收集；sleep(0) 不阻塞线程；协程不适合 CPU 密集）
- A5：B（`pct_change(1)` 环比；`pct_change(12)` 同比）
- A6：C（sqlite3 DB-API 使用 `?` 占位）
- A7：B（单行 JSON 便于观测与检索）
- A8：B（`popitem(False)` 淘汰最旧）
- A9：A（contextmanager 的 `yield` 前后对应进入/退出语义）
- A10：B（行流式读取 JSON）
- A11：B（`net=amount/(1+rate)；tax=amount-net`）
- A12：B（`MonthEnd(0)` 计算当月月末）

评分说明：作答正确得 1 分，错误或多选不得分。

---

## B. 多选题（每题 2 分，不给半分，全部正确得分）
- B1：A、C、D
- B2：A、C、D
- B3：A、B、C、D
- B4：A、B、C、D
- B5：A、C、D
- B6：A、B、D

---

## C. 判断题（每题 1 分）
- C1：对（list append 摊还 O(1)）
- C2：错（basicConfig 重复调用不生效，需显式配置 Handler）
- C3：对（同比 12 期）
- C4：错（sqlite3 参数化不使用 `$1`；使用 `?`/`:name`）
- C5：错（CPU 密集应使用进程或线程池 offload）
- C6：错（`popitem(False)` 是最旧，不是最新）

---

## D. 简答题（每题 4 分）
评分要点（示例）：
- D1 JSON 日志（每点 1 分，满 4 分）
  - 单行 JSON（结构化、易检索）；字段规范（ts/level/msg/trace_id/span_id/业务字段）
  - 时区与时精度（UTC、毫秒/微秒）
  - 异常结构化（type/message/stack）
  - 采样/脱敏策略（PII 处理）
- D2 contextvars（每点 1 分）
  - 线程/协程安全的上下文存储；trace_id/span_id 贯穿；中间件注入；日志取值
- D3 Decimal vs float（每点 1 分）
  - Decimal 可控舍入与精度；性能偏慢；推荐 `quantize('0.00')` + HALF_UP 或 HALF_EVEN（场景区分）
  - 金融金额展示与计算规则要一致（业务口径优先）
- D4 merge 后处理（每点 1 分）
  - 键 dtype 对齐；缺失填充；列名冲突重命名；下游计算前向量化
- D5 个税速算（每点 1 分）
  - 档位匹配；税额=应纳税所得额*税率-速算扣除；边界值包含关系；保留两位
- D6 重试与退避（每点 1 分）
  - 最大次数/超时；指数退避 + 抖动；可重试条件与幂等；错误记录与告警

---

## E. 代码阅读与改错（每题 5 分）
- E1 分块生成器（5 分）
  - 问题定位（2 分）：`yield` 后 `clear()` 清空已返回对象
  - 修复方案（2 分）：`yield buf; buf = []`
  - 边界说明（1 分）：尾块不足 n 也需返回
- E2 LRU 淘汰（5 分）
  - 找错（2 分）：应使用 `popitem(False)`
  - 解释（1 分）：最旧元素被淘汰
  - 补充（2 分）：命中需移动到尾；容量相等时淘汰
- E3 日志配置（5 分）
  - 找错（2 分）：级别/格式不符合要求
  - 修正（2 分）：`level=INFO, format='%(asctime)s - %(levelname)s - %(message)s'`
  - 说明（1 分）：重复 basicConfig 不生效，需清理或显式 Handler
- E4 月末偏移（5 分）
  - 找错（2 分）：使用 Day(31) 不可靠
  - 修正（2 分）：`MonthEnd(0)`
  - 说明（1 分）：跨月与大小月边界
- E5 SQL 注入（5 分）
  - 找错（2 分）：字符串拼接
  - 修正（2 分）：参数化 `WHERE code = ?`
  - 说明（1 分）：主键/唯一约束幂等

---

## F. 编程题（每题 8–10 分）
统一评分维度（建议）：正确性 5 分、鲁棒性 2 分、复杂度 1 分、代码风格 1 分、测试 1 分（合计 10 分，可按题型裁剪）
- F1 金额提取：正则 `(?:\d+(?:\.\d+)?)`；浮点转换；中文标点兼容；O(n)
- F2 部门汇总：聚合求和；浮点保留 2 位；部门集+推导；稳定
- F3 多键排序：`key=(parsed_date, -amount)`；O(n log n)
- F4 CSV 拆税：`tax=round(amount*rate/(1+rate),2)`；`DictReader/Writer`；保表头
- F5 pandas 拆分：向量化 `to_numpy`/`np.round`；避免 `apply`
- F6 asyncio 限流：`Semaphore(limit)`；`gather` 并发收集；异常处理
- F7 规则引擎：`match` 支持操作符；`apply_actions` set/compute_tax；叠加动作
- F8 网格 BFS：队列 `popleft`；访问标记；不可达 -1

---

## G. SQL 题（每题 6–8 分）
评分维度：正确性 4、语法规范 2、性能/可读性 2
- G1 左连接+汇总
```sql
SELECT IFNULL(o.dept,'UNK') AS dept, SUM(i.amount) AS amount_sum
FROM invoices i LEFT JOIN org o ON i.code=o.code AND i.number=o.number
GROUP BY dept ORDER BY dept;
```
- G2 2024-03 期间总额
```sql
SELECT SUM(amount) FROM invoices WHERE substr(date,1,7) = '2024-03';
```
- G3 period+dept 汇总（含税→税额拆分）
```sql
SELECT substr(date,1,7) AS period, dept,
       SUM(amount) AS amount_sum,
       SUM(amount - amount/(1+rate)) AS tax_sum
FROM invoices GROUP BY period, dept ORDER BY period, dept;
```
- G4 左差集（invoices- org）
```sql
SELECT i.* FROM invoices i
LEFT JOIN org o ON i.code=o.code AND i.number=o.number
WHERE o.code IS NULL;
```
- G5 去重统计（示例：聚合）
```sql
SELECT code, number, MIN(date) AS first_date, SUM(amount) AS amount_sum
FROM invoices GROUP BY code, number;
```

---

## H. 系统/API 设计（每题 8–10 分）
评分要点示例：
- 契约清晰（路由/参数/响应/错误码），幂等（主键/去重），日志（JSON+trace/span），校验（金额非负/税率集合/日期范围），安全（限流/采样/脱敏）

---

## I. 财税业务综合（每题 8–12 分）
评分要点示例：
- 计算口径正确、边界（档位/期间）、可观测性（日志）、测试（断言/随机用例）、鲁棒性（空/坏行）

---

## 备注
- 本答案版为参考实现与评分要点，实际阅卷可结合岗位级别细化 rubric（例如：并发题增加“异常聚合与背压”的权重，SQL 题增加“索引与窗口函数”的讨论）
