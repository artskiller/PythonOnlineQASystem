# 🚀 税务师事务所 AI 工程师面试冲刺指南

## 📅 7天冲刺计划（AI技能增强版）

### Day 1: AI技能基础 ⭐⭐⭐ 【新增】

**目标**：掌握机器学习和NLP基础，这是AI工程师的核心技能

#### 上午（3小时）：机器学习基础
```bash
# 1. 学习速查卡（30分钟）
cat AI_CHEATSHEET.md

# 2. 练习 Set ML1（2小时）
cd interview_exercises
python set_ML1_blank.py

# 3. 对照答案（30分钟）
cat set_ML1_answers.py
```

**重点内容**：
- ✅ 特征工程：OneHot编码、Label编码、标准化、归一化、分箱
- ✅ 模型训练：LogisticRegression、RandomForest
- ✅ 模型评估：准确率、精确率、召回率、F1、AUC
- ✅ 交叉验证：cross_val_score
- ✅ 实战：税务风险分类

#### 下午（3小时）：NLP基础
```bash
# 1. 安装依赖
pip install jieba scikit-learn

# 2. 练习 Set NLP1（2小时）
python set_NLP1_blank.py

# 3. 对照答案（1小时）
cat set_NLP1_answers.py
```

**重点内容**：
- ✅ 中文分词：jieba.lcut()、自定义词典
- ✅ 文本特征：TF-IDF、余弦相似度
- ✅ 文本分类：LogisticRegression + TfidfVectorizer
- ✅ 信息提取：正则表达式提取金额、日期、公司名
- ✅ 实战：发票描述分类

#### 晚上（2小时）：OCR基础
```bash
# 1. 练习 Set OCR1（1.5小时）
python set_OCR1_blank.py

# 2. 对照答案（30分钟）
cat set_OCR1_answers.py
```

**重点内容**：
- ✅ 图像预处理：灰度化、二值化、去噪、缩放
- ✅ OCR识别：PaddleOCR/Tesseract（可选）
- ✅ 字段提取：发票号、代码、日期、金额
- ✅ 错误纠正：OCR常见错误（O/0混淆）
- ✅ 实战：发票批量识别

**Day 1 总结**：
- ✅ 完成3个AI专项套题（ML1、NLP1、OCR1）
- ✅ 掌握AI工程师核心技能
- ✅ 为财税AI应用打下基础

---

### Day 2: 财税业务专项突击 🔥

#### 上午（3小时）
```bash
# 学习财税核心概念
cat INTERVIEW_READINESS_ANALYSIS.md

# 练习个税计算
cd exercises/06_business
python set_E_blank.py  # 个税/增值税/发票解析

# 查看详细注释
cat set_E_answers_annotated.py
```

**重点掌握**：
- ✅ 个税速算扣除公式：`税额 = 应纳税所得额 × 税率 - 速算扣除`
- ✅ 增值税计算：`税额 = 含税金额 - 含税金额/(1+税率)`
- ✅ 发票号/税号正则匹配
- ✅ Luhn校验算法

#### 下午（3小时）
```bash
# 业务进阶练习
python set_J_blank.py  # 发票去重/JSON Lines/税率分类

# 高精度计算
python set_F_blank.py  # Decimal/舍入/格式化

# 数据合规
python set_Q_blank.py  # 脱敏/校验/规则引擎
```

**重点掌握**：
- ✅ Decimal 高精度计算
- ✅ 银行家舍入 vs 四舍五入
- ✅ 数据脱敏策略
- ✅ 统一社会信用代码校验

#### 晚上（2小时）
```bash
# 整理知识点
# 创建速查卡片
```

**输出**：
- 个税税率表（7档）
- 增值税税率表（13%, 9%, 6%, 3%）
- 常用正则表达式
- 常见陷阱清单

---

### Day 3: 数据处理与并发 💪

#### 上午（3小时）
```bash
# pandas 数据处理
cd exercises/02_data
python set_B_blank.py  # pandas 基础
python set_G_blank.py  # pandas 进阶

# 查看进度
python ../../progress.py --show
```

**重点掌握**：
- ✅ `merge/join/concat` 区别
- ✅ `groupby/agg/pivot_table`
- ✅ `pct_change/diff/shift` 环比同比
- ✅ 缺失值处理 `fillna/dropna`
- ✅ 日期处理 `pd.to_datetime/MonthEnd`

#### 下午（3小时）
```bash
# 并发编程
cd exercises/04_concurrency
python set_D_blank.py  # 线程池/asyncio/numpy
python set_H_blank.py  # 协程并发
python set_T_blank.py  # 异步编排
```

**重点掌握**：
- ✅ `ThreadPoolExecutor` 用法
- ✅ `asyncio.gather/create_task`
- ✅ `asyncio.Semaphore` 限流
- ✅ `await` 与 `async def`
- ✅ NumPy 向量化计算

---

### Day 4: 系统设计与工程实践 🏗️

#### 上午（3小时）
```bash
# API 设计
cd exercises/07_system
python set_S_blank.py  # RESTful API
python set_U_blank.py  # 异步编排

# 日志与追踪
cd exercises/05_engineering
python set_L_blank.py  # 日志配置
python set_N_blank.py  # 结构化日志
python set_P_blank.py  # 异常处理
```

**重点掌握**：
- ✅ JSON 日志格式
- ✅ trace_id/span_id 传递
- ✅ 异常结构化
- ✅ 上下文管理器 `@contextmanager`

#### 下午（3小时）
```bash
# 综合练习
python set_R_blank.py  # 缓存/重试
python set_V_blank.py  # 分布式追踪
python set_W_blank.py  # 监控指标
```

---

### Day 5: 模拟面试（AI+财税混合）🎯

#### 上午（2.5小时）
```bash
# 第一次模拟面试（侧重AI技能）
python interview_simulator.py --duration 120 --focus ai
```

**要求**：
- ⏱️ 严格限时120分钟
- 🚫 不查看答案
- 📝 记录卡住的题目
- ⏰ 记录每题用时

#### 下午（2小时）
```bash
# 分析第一次模拟结果
cat interview_results/interview_*/report.json

# 复习错题
# 查看答案注释版
```

#### 晚上（2.5小时）
```bash
# 第二次模拟面试（侧重财税）
python interview_simulator.py --duration 120 --focus tax
```

**对比**：
- 第一次 vs 第二次得分
- 时间管理改进
- 错误类型分析

---

### Day 6: 综合模拟与AI实战 🚀

#### 上午（2.5小时）
```bash
# 第三次模拟面试（AI+财税混合）
python interview_simulator.py --duration 120 --random 5
```

**要求**：
- ⏱️ 严格限时120分钟
- 🎯 随机抽取5套题目
- 📊 记录完成情况

#### 下午（3小时）
```bash
# AI实战练习
cd interview_exercises

# 完整流程练习
python set_ML1_blank.py   # 机器学习
python set_NLP1_blank.py  # NLP
python set_OCR1_blank.py  # OCR
```

**重点**：
- ✅ 完整的ML pipeline（特征工程→训练→评估）
- ✅ 文本分类完整流程
- ✅ OCR字段提取与校验

#### 晚上（2小时）
```bash
# 复习AI速查卡
cat AI_CHEATSHEET.md

# 复习财税速查卡
cat TAX_CHEATSHEET.md
```

---

### Day 7: 查漏补缺与心态调整 🎓

#### 上午（3小时）
```bash
# 错题本复习
# 重做所有失败的题目

# 速查卡复习
# 背诵关键公式和API
```

**检查清单**：
- [ ] **AI技能**：特征工程、模型训练、评估指标
- [ ] **NLP**：jieba分词、TF-IDF、文本分类
- [ ] **OCR**：图像预处理、字段提取、错误纠正
- [ ] **个税**：7档税率表、速算扣除
- [ ] **增值税**：计算公式、税率档次
- [ ] **pandas**：groupby、pivot_table、merge
- [ ] **asyncio**：async/await、gather、Semaphore
- [ ] **正则表达式**：发票号、税号、金额提取
- [ ] **Decimal**：ROUND_HALF_UP vs ROUND_HALF_EVEN

#### 下午（2小时）
```bash
# 最后一次模拟（随机题目）
python interview_simulator.py --random 5 --duration 60
```

**目标**：
- 得分 >= 80%
- 时间充裕（提前完成）
- 心态平稳

#### 晚上（1小时）
- 整理面试用品
- 检查开发环境
- 早睡，保证状态

---

## 🎯 面试当天策略

### 时间分配（120分钟）

| 阶段 | 时间 | 任务 |
|------|------|------|
| 浏览 | 0-5分钟 | 快速浏览所有题目，标记难度 |
| 第一轮 | 5-35分钟 | 完成所有简单题（预计10-15题） |
| 第二轮 | 35-75分钟 | 完成中等难度题（预计5-8题） |
| 第三轮 | 75-105分钟 | 攻克困难题（预计3-5题） |
| 检查 | 105-120分钟 | 运行测试，修复错误 |

### 答题顺序

**优先级排序**：
1. ⭐⭐⭐ 财税业务题（展示专业匹配度）
2. ⭐⭐ 简单填空题（快速得分）
3. ⭐⭐ 数据处理题（常见考点）
4. ⭐ 并发编程题（中等难度）
5. ⭐ 系统设计题（时间充裕再做）

### 调试技巧

```python
# 1. 快速打印调试
print(f"DEBUG: {variable=}")  # Python 3.8+
print(f"DEBUG: type={type(obj)}, value={obj}")

# 2. 断言验证
assert isinstance(result, list), f"Expected list, got {type(result)}"
assert len(result) > 0, "Result should not be empty"

# 3. 边界测试
test_cases = [
    (0, expected_0),
    (1, expected_1),
    (-1, expected_neg),
    (None, expected_none),
]
for input_val, expected in test_cases:
    result = func(input_val)
    assert result == expected, f"Failed for {input_val}"

# 4. 类型提示检查
from typing import List, Dict
def func(data: List[Dict]) -> float:
    ...
```

### 常见陷阱

#### 1. 个税计算
```python
# ❌ 错误：忘记速算扣除
tax = taxable * rate

# ✅ 正确：使用速算扣除
tax = taxable * rate - quick_deduction
```

#### 2. 增值税计算
```python
# ❌ 错误：直接乘税率
tax = amount * rate

# ✅ 正确：含税金额需要先换算
tax = amount - amount / (1 + rate)
```

#### 3. pandas 缺失值
```python
# ❌ 错误：忘记处理 NaN
df.groupby('dept')['amount'].sum()

# ✅ 正确：先填充或删除
df.fillna(0).groupby('dept')['amount'].sum()
```

#### 4. asyncio 忘记 await
```python
# ❌ 错误：忘记 await
result = async_func()  # 返回 coroutine 对象

# ✅ 正确：使用 await
result = await async_func()
```

---

## 📋 速查卡

### 个税税率表（简化）
| 应纳税所得额 | 税率 | 速算扣除 |
|-------------|------|---------|
| ≤ 36,000 | 3% | 0 |
| ≤ 144,000 | 10% | 2,520 |
| ≤ 300,000 | 20% | 16,920 |
| ≤ 420,000 | 25% | 31,920 |
| ≤ 660,000 | 30% | 52,920 |
| ≤ 960,000 | 35% | 85,920 |
| > 960,000 | 45% | 181,920 |

### 增值税税率
- 13%：销售货物、加工修理修配劳务
- 9%：交通运输、邮政、建筑、不动产租赁
- 6%：现代服务、金融服务、生活服务
- 3%：小规模纳税人

### 常用正则
```python
# 整数或小数
r"\d+(?:\.\d+)?"

# 发票号（8-12位数字）
r"\d{8,12}"

# 税号（15-20位大写字母数字）
r"[A-Z0-9]{15,20}"

# 统一社会信用代码（18位）
r"[0-9A-Z]{18}"

# 账号脱敏（保留末4位）
r"(\d{6,15})(\d{4})"
```

### pandas 常用操作
```python
# 环比
df['pct'] = df['amount'].pct_change(1)

# 同比
df['yoy'] = df['amount'].pct_change(12)

# 月末
df['month_end'] = pd.to_datetime(df['date']) + pd.offsets.MonthEnd(0)

# 透视表
df.pivot_table(values='amount', index='period', columns='dept', aggfunc='sum')

# 左连接
pd.merge(left, right, on='key', how='left')
```

### asyncio 常用模式
```python
# 并发执行
results = await asyncio.gather(task1(), task2(), task3())

# 限流
sem = asyncio.Semaphore(5)
async with sem:
    await api_call()

# 超时
await asyncio.wait_for(task(), timeout=10)
```

---

## 💡 心态调整

### 面试前
- ✅ 充足睡眠（7-8小时）
- ✅ 正常饮食，避免过饱
- ✅ 提前30分钟到达
- ✅ 深呼吸，放松心情

### 面试中
- ✅ 遇到难题不慌张，先跳过
- ✅ 相信自己的准备
- ✅ 时间管理优先于完美答案
- ✅ 保持冷静，逐题攻克

### 面试后
- ✅ 不纠结已完成的题目
- ✅ 总结经验，为下次准备
- ✅ 保持积极心态

---

## ✅ 最后检查清单

### 知识准备
- [ ] 个税计算公式熟练
- [ ] 增值税计算公式熟练
- [ ] pandas 常用操作熟练
- [ ] asyncio 基本模式熟练
- [ ] 正则表达式熟练
- [ ] Decimal 使用熟练

### 技能准备
- [ ] 完成至少2次完整模拟
- [ ] 得分稳定在 80%+
- [ ] 时间管理良好
- [ ] 调试技巧熟练

### 环境准备
- [ ] Python 环境正常
- [ ] 编辑器配置好
- [ ] 快捷键熟悉
- [ ] 网络连接稳定

### 心理准备
- [ ] 充足睡眠
- [ ] 心态平稳
- [ ] 自信满满
- [ ] 准备充分

---

**祝你面试成功！🎉**

