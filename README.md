# 🐍 Python 学习项目 - 从入门到精通

<div align="center">

**系统化的 Python 学习路径 | 28 套精心设计的练习 | 涵盖基础到高级的完整知识体系**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[🚀 开始使用](GETTING_STARTED.md) • [快速开始](QUICK_START.md) • [学习路径](LEARNING_PATH.md) • [知识图谱](KNOWLEDGE_MAP.md) • [常见问题](FAQ.md)

</div>

---

## 🎉 项目更新

> **最新消息（2025-11-05）**：项目已完成学习友好化改造 + 面试准备增强 + **AI技能专项增强**！
>
> **学习系统**：
> - ✅ 新增 8 个阶段的系统化学习路径
> - ✅ 新增交互式学习工具（`learn.py`）
> - ✅ 新增进度追踪系统（`progress.py`）
> - ✅ 新增完整的文档体系（15500+ 字）
> - ✅ 新增分级目录结构（84 个符号链接）
>
> **面试准备**（🔥 新增）：
> - ✅ 面试模拟器（`interview_simulator.py`）- 2小时限时练习
> - ✅ 面试准备度分析（`INTERVIEW_READINESS_ANALYSIS.md`）
> - ✅ 7天冲刺指南（`INTERVIEW_SPRINT_GUIDE.md`）
> - ✅ 财税知识速查卡（`TAX_CHEATSHEET.md`）
>
> **AI技能增强**（⭐ 最新）：
> - ✅ 机器学习基础套题（`set_ML1`）- 特征工程/模型训练/评估
> - ✅ NLP基础套题（`set_NLP1`）- 中文分词/TF-IDF/文本分类
> - ✅ OCR实战套题（`set_OCR1`）- 图像预处理/字段提取/批量识别
> - ✅ AI技能速查卡（`AI_CHEATSHEET.md`）
> - ✅ AI技能缺口分析（`AI_SKILLS_GAP_ANALYSIS.md`）
>
> 查看 [AI技能增强总结](AI_ENHANCEMENT_SUMMARY.md) 了解详情

---

## 📖 项目简介

这是一个**系统化的 Python 学习项目**，包含 28 套精心设计的练习题，涵盖从基础语法到系统设计的完整知识体系。

### ✨ 项目特色

- 🎯 **渐进式学习路径** - 8 个阶段，从入门到精通
- 💡 **交互式学习工具** - 提供提示系统和即时反馈
- 📊 **进度追踪系统** - 可视化学习进度
- 🔍 **三种版本对照** - 空白版、答案版、注释版
- 🌳 **完整知识图谱** - 清晰的知识点关联
- 🎓 **实战项目导向** - 3 个端到端综合项目

### 📚 涵盖内容

| 阶段 | 主题 | 套题 | 难度 | 时间 |
|------|------|------|------|------|
| 1️⃣ | **基础入门** | A, K | ⭐ | 2-3 天 |
| 2️⃣ | **数据处理** | B, G | ⭐⭐ | 3-4 天 |
| 3️⃣ | **算法思维** | C, I, O | ⭐⭐⭐ | 4-5 天 |
| 4️⃣ | **并发编程** | D, H, T | ⭐⭐⭐ | 3-4 天 |
| 5️⃣ | **工程实践** | L, N, P, M | ⭐⭐ | 3-4 天 |
| 6️⃣ | **业务应用** | E, J, F, Q | ⭐⭐⭐ | 3-4 天 |
| 7️⃣ | **系统设计** | R, S, U, V, W, X, Y | ⭐⭐⭐ | 4-5 天 |
| 8️⃣ | **综合项目** | Z, AA, AB | ⭐⭐⭐⭐ | 5-7 天 |
| 🤖 | **AI专项** | ML1, NLP1, OCR1 | ⭐⭐⭐ | 2-3 天 |

**总计**：31 套题 × 3 版本 = 93 个练习文件

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/pythonLearn.git
cd pythonLearn
```

### 2. 环境设置（2 分钟）

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 开始学习（选择一种方式）

##### 方式 A：交互式学习（推荐新手）

```bash
python learn.py --level 01
```

#### 方式 B：直接练习（推荐有经验者）

```bash
# 编辑空白版
vim exercises/01_basics/set_A_blank.py

# 运行测试
python exercises/01_basics/set_A_blank.py
```

#### 方式 C：AI技能专项练习（推荐AI工程师）

```bash
# 机器学习基础
cd interview_exercises
python set_ML1_blank.py

# NLP基础
python set_NLP1_blank.py

# OCR实战
python set_OCR1_blank.py
```

#### 方式 D：查看答案学习（推荐复习）

```bash
# 查看带注释的答案
cat exercises/01_basics/set_A_answers_annotated.py
```

### 4. 查看进度

```bash
python progress.py --show
```

**详细指南**：查看 [快速开始文档](QUICK_START.md)

---

## 📊 学习路径

### 系统学习路径（推荐）

```
第1阶段：基础入门 (A, K)
   ↓
第2阶段：数据处理 (B, G)
   ↓
第3阶段：算法思维 (C, I, O)
   ↓
第4阶段：并发编程 (D, H, T)
   ↓
第5阶段：工程实践 (L, N, P, M)
   ↓
第6阶段：业务应用 (E, J, F, Q)
   ↓
第7阶段：系统设计 (R, S, U, V, W, X, Y)
   ↓
第8阶段：综合项目 (Z, AA, AB)
```

### 快速路径（面试冲刺）

```
A (基础) → B (pandas) → C (算法) → D (并发) → P (日志) → Z (项目)
```

**预计时间**：2-3 周

### 专项路径

**数据分析**：`A → B → G → E → J → Z`

**后端开发**：`A → C → D → H → P → S → T → AA → AB`

**算法工程师**：`A → C → I → O → D → H → T`

**详细路径**：查看 [学习路径文档](LEARNING_PATH.md)

---

## 🎯 核心知识点

<details>
<summary><b>点击展开完整知识点列表</b></summary>

### 基础与标准库
- 正则表达式、字典/集合推导
- 生成器与迭代器、上下文管理器
- CSV 处理、文件 I/O

### 数据处理
- pandas: DataFrame、groupby、merge
- 向量化计算、时间序列
- 环比同比、滚动窗口、透视表

### 算法与数据结构
- LRU Cache、Trie、并查集
- 二分查找、BFS/DFS
- KMP、滑动窗口、快速选择

### 并发编程
- asyncio: 协程、事件循环
- 并发控制：Semaphore、Queue
- 重试退避、线程安全

### 工程实践
- 结构化日志、异常处理
- 类型注解、Protocol
- 测试与调试

### 业务应用
- 个税/增值税计算
- 发票解析与校验
- 数据脱敏与合规
- Decimal 高精度计算

### 系统设计
- SQLite 与 SQL 安全
- RESTful API 设计
- 链路追踪、数据流水线
- 规则引擎

</details>

**完整知识图谱**：查看 [知识图谱文档](KNOWLEDGE_MAP.md)

---

## 📁 项目结构

```
pythonLearn/
├── README.md                    # 项目总览（本文件）
├── QUICK_START.md              # 快速开始指南
├── LEARNING_PATH.md            # 详细学习路径
├── KNOWLEDGE_MAP.md            # 知识图谱
├── FAQ.md                      # 常见问题解答
├── requirements.txt            # 依赖列表
├── learn.py                    # 交互式学习工具（即将推出）
├── progress.py                 # 进度追踪工具（即将推出）
│
├── exercises/                  # 练习题目录（即将重组）
│   ├── 01_basics/             # 第1阶段：基础入门
│   ├── 02_data/               # 第2阶段：数据处理
│   ├── 03_algorithm/          # 第3阶段：算法思维
│   ├── 04_concurrency/        # 第4阶段：并发编程
│   ├── 05_engineering/        # 第5阶段：工程实践
│   ├── 06_business/           # 第6阶段：业务应用
│   ├── 07_system/             # 第7阶段：系统设计
│   └── 08_projects/           # 第8阶段：综合项目
│
└── interview_exercises/        # 原始题目（保留兼容）
    ├── README.md
    ├── set_A_blank.py
    ├── set_A_answers.py
    ├── set_A_answers_annotated.py
    └── ...
```

---

## 💡 学习建议

### 时间安排

- **全职学习**：4-6 周完成全部内容
- **业余学习**：8-12 周完成全部内容
- **面试冲刺**：2-3 周完成核心内容

### 学习方法

1. **先理解再动手** - 阅读题目要求，理解考察点
2. **独立完成** - 尽量不看答案，实在卡住再看提示
3. **对比优化** - 完成后对比答案版，学习更优写法
4. **举一反三** - 修改参数和场景，测试边界情况
5. **定期复习** - 每周回顾已完成的题目

### 遇到困难时

```bash
# 1. 获取提示
python learn.py --hint --question A1

# 2. 查看 FAQ
cat FAQ.md

# 3. 查看知识图谱
cat KNOWLEDGE_MAP.md

# 4. 查看详细注释
cat exercises/01_basics/set_A_answers_annotated.py
```

---

## 🛠️ 工具与命令

### 一键运行所有测试

```bash
# 运行答案版（验证环境）
python interview_exercises/run_all.py --mode answers

# 运行空白版（检查进度）
python interview_exercises/run_all.py --mode blank

# 使用 Makefile
make answers
```

### 交互式学习（即将推出）

```bash
# 启动交互式学习
python learn.py --level 01

# 获取提示
python learn.py --hint --question A1 --level 2

# 调试模式
python learn.py --debug --question A1
```

### 进度追踪（即将推出）

```bash
# 查看总体进度
python progress.py --show

# 查看本周进度
python progress.py --week

# 复习错题
python learn.py --review-mistakes
```

---

## 🎓 学习目标

完成本项目后，你将能够：

- ✅ 熟练使用 Python 标准库解决常见问题
- ✅ 使用 pandas 进行数据分析和处理
- ✅ 实现常见算法和数据结构
- ✅ 编写异步和并发代码
- ✅ 遵循工程最佳实践（日志、异常、测试）
- ✅ 理解业务场景并实现业务逻辑
- ✅ 设计和实现完整的系统组件
- ✅ 独立完成端到端项目

---

## 📚 补充资源

- **Python 官方文档**：https://docs.python.org/zh-cn/3/
- **pandas 文档**：https://pandas.pydata.org/docs/
- **asyncio 教程**：https://docs.python.org/zh-cn/3/library/asyncio.html
- **LeetCode 中文**：https://leetcode.cn/

---

## 🤝 贡献指南

欢迎贡献！你可以：

- 🐛 报告问题或建议
- 📝 改进文档
- ✨ 添加新的练习题
- 🔧 优化现有代码

**贡献步骤**：
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

<div align="center">

**准备好开始学习了吗？**

[🚀 立即开始](QUICK_START.md) | [📖 查看学习路径](LEARNING_PATH.md) | [❓ 常见问题](FAQ.md)

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

</div>
