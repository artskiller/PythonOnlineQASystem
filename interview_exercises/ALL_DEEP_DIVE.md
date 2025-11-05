# 面试套题手工精讲（Why vs How / 复杂度 / 边界 / 替代实现 / 测试）

说明：本文件对目录下所有套题（A–Z、AA、AB）进行“手工精讲”。每套题以同一结构展开：题目综述、Why vs How 要点、复杂度与性能、边界与易错、替代实现、测试用例清单。代码参考对应的答案文件 `set_?_answers.py` 与注解版 `set_?_answers_annotated.py`。

---

## A 基础与标准库（正则/排序/生成器/上下文/CSV）
- 题目综述
  - 金额提取、部门聚合、多键排序、行清洗、目录上下文、CSV 增列写出。
- Why vs How
  - Why：以标准库优先完成常见数据清洗与 I/O；How：正则非捕获组提数、`sorted(key=(date,-amount))`、生成器保流式、`@contextmanager` 保证退出恢复、`DictWriter` 统一表头。
  - 正则选 `(?:\d+(?:\.\d+)?)` 避免嵌套捕获污染；排序用 `datetime.strptime` 获得可比较对象。
- 复杂度与性能
  - 提取与清洗 O(n)；排序 O(n log n)；CSV 流式 O(n) 且常数低。
- 边界与易错
  - 金额中“中文逗号/空白/混排”；排序金额需降序（负号）；上下文异常也要恢复 cwd；CSV 字段缺失时注意 `reader.fieldnames` 为空的情况。
- 替代实现
  - 金额提取可用 `finditer` 减少中间列表；日期可用 `fromisoformat`（YYYY-MM-DD）。
- 测试清单
  - 空行/中文标点；相同日期不同金额；空 CSV 表头；异常退出后 cwd 恢复。

---

## B pandas 数据处理（读取/聚合/合并/向量化/时间）
- 题目综述
  - 多 sheet 合并、分组聚合、左连接补缺、向量化拆税、期间与月末、正则列提取。
- Why vs How
  - Why：pandas 适合表格数据批处理；How：`concat` 统一 dtype，`groupby(...).agg(...)` 可读，`merge(how='left')` 保左表，`to_period('M')+MonthEnd(0)` 求月末。
- 复杂度与性能
  - `groupby`/`merge` 近似 O(n)（由实现与键分布决定），优于 Python 循环；向量化避免 `apply`。
- 边界与易错
  - 键类型不一致导致空连接；`NaN` 填充值；`month_end` 需要 offset 而非简单 day=31；浮点舍入显示差异。
- 替代实现
  - `assign` 链式写法；`where`/`mask` 替代 `apply`；`Categorical` 限定分组维度。
- 测试清单
  - 键缺失/类型错；全空列；跨月与月末准确性；长整型代码保持为字符串。

---

## C 算法与 Pythonic（LRU/堆/生成器/二分/groupby/dataclass）
- 题目综述
  - LRU、TopK、递归扁平化、二分上界、RLE、数据类排序。
- Why vs How
  - LRU 用 `OrderedDict` O(1) 移动+淘汰；TopK 用小顶堆 O(n log k)；`yield from` 递归清爽；二分上界“满足则收缩右边界”。
- 复杂度与性能
  - LRU get/put O(1) 摊还；TopK O(n log k)；二分 O(log n)。
- 边界与易错
  - LRU `popitem(False)` 才是最旧；扁平化需限定容器类型；二分边界 `l<r`、返回 `l`。
- 替代实现
  - LRU 可用 `functools.lru_cache`（不适合自定义容量逐出控制）；TopK 可用 `nlargest`。
- 测试清单
  - LRU 淘汰顺序；TopK 频次并列稳定性；二分在重复元素上的定位。

---

## D 并发与性能（线程池/asyncio/numpy/分块/去重/日志）
- 题目综述
  - 线程池 I/O 并发、`asyncio.gather`、NumPy 拆税、分块生成器、保序去重、日志配置。
- Why vs How
  - I/O 用线程池；协程用 gather 并发收集；分块 `yield buf; buf=[]` 避免清空已返回对象；日志格式统一含时间/级别/消息。
- 复杂度与性能
  - 线程池加速 I/O；分块降低峰值内存；NumPy 向量化显著减少 Python 开销。
- 边界与易错
  - 分块误用 `clear`；协程未 `await`；日志多次 `basicConfig` 无效需直接配置 Handler。
- 替代实现
  - `concurrent.futures.as_completed` 控制回收；`map` 保序。
- 测试清单
  - 分块边界 n=1/大于长度；线程数变化；日志多次初始化。

---

## E 业务综合（个税/增值税/发票解析/脱敏/报表）
- Why vs How
  - 个税使用“当前档速算扣除”；增值税税额=含税-不含税；正则命名组提取字段；脱敏保留末 4 位；报表按 period/dept 透视。
- 复杂度与性能
  - 均为 O(n)；正则多行需注意惰性匹配。
- 边界与易错
  - 档位边界值；大小写/中文字符；金额转 float 的精度展示；缺列填默认值。
- 替代实现
  - Decimal 处理金额；正则 `finditer` 精准定位多条。
- 测试清单
  - 速算边界、不同税率、发票文本多行无序、脱敏长度 10~19。

---

## F 文本与高精度（Decimal/多行正则/上下文/格式化/聚合/校验）
- Why vs How
  - 金额选 Decimal 控制舍入；`localcontext` 临时设置 rounding；多行 `finditer`；金额千分位格式化使用 `:,`。
- 复杂度与性能
  - Decimal 比 float 慢，但金融场景值得；正则 O(n)。
- 边界与易错
  - 舍入模式差异（HALF_UP vs HALF_EVEN）；本地化/小数位统一。
- 替代实现
  - `quantize(Decimal('0.00'))` 控制位数；`context` 做批量计算。

---

## G pandas 进阶（类型/分类/环比同比/滚动/透视合计/时区）
- Why vs How
  - `parse_dates`/`dtype` 保证键一致；`astype('category')` 限制取值；`pct_change(1|12)` 环比同比；`rolling(...).mean()`；`sum(axis=1)` 行合计；`tz_localize('UTC').tz_convert('Asia/Shanghai')`。
- 边界与易错
  - 首行 NaN、分类未覆盖新值、时区重复转换报错。
- 测试清单
  - 目录同上并包含 DST 切换日。

---

## H 并发进阶（限流/线程安全计数器/指数退避/生产者消费者）
- Why vs How
  - 协程限流用 `Semaphore`；计数器加锁防竞态；退避采用指数乘 2 + 抖动；有限队列背压。
- 边界与易错
  - 未 `task_done` 会阻塞 join；退避上限控制；消费者结束哨兵。

---

## I 算法进阶（Trie/并查集/KMP/滑窗/快速选择/拓扑）
- Why vs How
  - Trie 掩码按匹配区间置 `*`；并查集路径压缩+按秩；KMP 前缀函数；滑窗用哈希最后位置；快选按目标下标；Kahn 拓扑。
- 复杂度
  - Trie O(总长度)；并查集近乎 O(1)；KMP O(n+m)；滑窗 O(n)；快选 O(n) 期望；拓扑 O(n+m)。
- 边界
  - Trie 重叠匹配；KMP 空模式；拓扑检测环。

---

## J 业务进阶（近似去重/JSONL/税率标签/CSV 汇总/信用代码/舍入）
- Why vs How
  - 近似去重按键+金额阈值；JSONL 流式；税率标签快速 bucketing；银行家舍入 vs 四舍五入对比。
- 边界
  - 浮点阈值比较；邮箱/编码大小写；CSV 排序稳定性。

---

## K 混合题型（选择/判断/实现/预测/小脚本）
- Why vs How
  - 性能常识：dict 查 O(1)、list 查 O(n)；浅拷贝只拷最外层；手机号保留末 11 位；预测考察“扩展后再修改原列表不影响副本”。

---

## L 调试与修复（合并/路径/分块/日志）
- Why vs How
  - 合并需拷贝避免副作用；路径用 `os.path.join`；分块切片递进；日志 INFO + `%(asctime)s`。

---

## M 设计与文档（dataclass/聚合/协议/文档）
- Why vs How
  - 排序字段用隐藏键，保证 `currency` 升序、`amount` 降序；聚合幂等；Protocol 体现结构化子类型；文档强调“幂等/边界”。

---

## N 异常与上下文（文件写入包装/重试装饰器/语义）
- Why vs How
  - 失败包装统一错误前缀；重试固定间隔与最大次数；`try/else/finally`：else 在无异常时运行，finally 总执行。

---

## O 算法与实战（网格最短路/日志解析/令牌化/JSON 分组）
- Why vs How
  - 最短路 BFS 用队列 popleft；日志正则提 level；令牌化保中文与数字；分组 `setdefault`。
- 边界
  - BFS 不可遍历障碍；日志大小写统一；中文全角标点。

---

## P 日志与可观测性（JSON 日志/采样/耗时/上下文）
- Why vs How
  - 单行 JSON 便于搜索；采样过滤减量；耗时使用 `perf_counter`；`contextvars` 注入 request_id。

---

## Q 脱敏与合规（哈希/姓名/邮箱/k-匿名/身份证格式）
- Why vs How
  - 哈希+盐抗彩虹表；姓名/邮箱最小必要展示；k-匿名每组≥k；身份证 18 位末位校验字符 X。

---

## R SQLite 与 SQL 安全（参数化/主键/左连接）
- Why vs How
  - `INSERT OR IGNORE/REPLACE` 控制幂等；参数化避免注入；左连接与 `IFNULL` 处理缺部门。
- 边界
  - 主键冲突；空聚合返回 None；编码与 locale。

---

## S API 契约（纯标准库 HTTP/参数校验/错误码）
- Why vs How
  - 明确路由与错误码；查询参数用 `parse_qs`；JSON 体严格字段类型；税额拆分与舍入。

---

## T 异步任务编排（去重/背压/重试/优雅关闭）
- Why vs How
  - 去重用 key 集合；队列 `maxsize` 背压；指数退避+抖动；`queue.join+cancel` 优雅退出。

---

## U Tracing 模拟（trace/span/事件）
- Why vs How
  - 以 `contextvars` 模拟跨调用上下文；span 栈管理进出；事件附带 trace_id/span_id。

---

## V OCR 文本清洗（规范化/字段抽取）
- Why vs How
  - 全角转半角、货币符统一；常见 O→0 纠错仅限数字块；字段单独正则提高鲁棒性。

---

## W 批量导入流水线（校验→事务→回执）
- Why vs How
  - 校验先行；事务 `BEGIN/commit/rollback`；错误聚合回执；`REPLACE` 实现幂等导入。

---

## X 审计日志轮转（按大小/备份数）
- Why vs How
  - 先删最旧，再高号倒序移动，最后当前→.1；写入前判断大小，避免越界写后再搬迁。

---

## Y 简易规则引擎（条件匹配/动作执行）
- Why vs How
  - 条件支持 eq/ne/gt/gte/lt/lte/in；动作 `set`/`compute_tax`；按顺序叠加作用。

---

## Z 端到端小项目（CLI→校验→转换→落库→报表→日志）
- Why vs How
  - 分层：读/验/转/存/报/记；JSON 日志可观测；SQLite 保证幂等；period 聚合。
- 边界
  - 文件编码、表头缺失、日期越界、税率限集。

---

## AA 端到端·并发版（扫描→并发解析→集中落库→报表；隔离+重试）
- Why vs How
  - 线程池分摊 I/O；失败隔离记录日志；有限重试提升临时失败可用性；trace/span 贯穿链路，persist 独立 span。
- 复杂度与性能
  - 总体 O(总行数)；并发受 IO/CPU 限制；磁盘吞吐受限时收益递减。
- 边界
  - 错误文件/半行；字段缺失；日期/税率集合校验；吞吐与线程数权衡。

---

## AB 端到端·HTTP 服务版（POST /report → 校验→聚合→返回）
- Why vs How
  - 标准库 `http.server` 快速成型；严格校验（金额非负/税率集合/日期边界）；聚合返回 period,dept 汇总；提供 `/shutdown` 测试端点。
- 边界
  - 受限环境禁止监听（自检已降级跳过）；请求体大小与解析错误；并发连接（可扩展线程化）。

---

结语：
- 原则：先保证正确与可观测，再优化性能；以标准库与向量化为先，必要时用并发；所有 I/O 与外部交互都要明确边界与失败策略。
- 如需将本精讲拆分成每套题单独文件或导出 PDF，请告知需求格式与分卷策略。

