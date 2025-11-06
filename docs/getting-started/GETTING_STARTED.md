# 🚀 开始使用 - 5分钟快速上手

欢迎来到 Python 学习项目！本指南将帮助你在 5 分钟内开始学习。

---

## 📋 前置要求

- Python 3.8 或更高版本
- 基本的命令行使用经验
- 文本编辑器（推荐 VS Code、PyCharm 或 Vim）

---

## ⚡ 快速开始（3步）

### 第1步：初始化项目

```bash
# 克隆或进入项目目录
cd pythonLearn

# 一键初始化（创建虚拟环境、安装依赖、组织文件）
make setup

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows
```

### 第2步：查看学习进度

```bash
# 查看当前进度和建议
make progress
```

你会看到类似这样的输出：

```
📊 学习进度总览
======================================================================

⬜ 第01阶段：基础入门
   [░░░░░░░░░░░░░░░░░░░░] 0/2 题 (0%)
   预计时间：3.5 小时

💡 建议：从第1阶段开始学习
   运行：python learn.py --level 01
```

### 第3步：开始学习

```bash
# 启动第1阶段的学习
make learn LEVEL=01
```

你会看到详细的学习指导：

```
🎯 开始学习：第01阶段 - 基础入门

📝 掌握 Python 核心语法和标准库

💡 学习建议：
  1. 进入目录：cd exercises/01_basics
  2. 查看题目：cat set_A_blank.py
  3. 编辑填空：vim set_A_blank.py
  4. 运行测试：python set_A_blank.py
  5. 对比答案：diff set_A_blank.py set_A_answers.py
  6. 查看注释：cat set_A_answers_annotated.py
```

---

## 📚 学习流程

### 典型的学习循环

```
1. 查看题目 → 2. 编写代码 → 3. 运行测试 → 4. 查看答案 → 5. 理解注释
     ↑                                                              ↓
     └──────────────────────── 重复直到通过 ←─────────────────────┘
```

### 详细步骤

#### 1️⃣ 查看题目

```bash
cd exercises/01_basics
cat set_A_blank.py
```

#### 2️⃣ 编写代码

用你喜欢的编辑器打开 `set_A_blank.py`，填写 `pass` 处的代码：

```python
def extract_amounts(text: str) -> list[float]:
    """从文本中提取所有金额（整数或小数）"""
    pass  # ← 在这里编写你的代码
```

#### 3️⃣ 运行测试

```bash
python set_A_blank.py
```

如果通过，你会看到：
```
✅ All tests passed!
```

如果失败，你会看到错误信息。

#### 4️⃣ 获取提示（如果卡住了）

```bash
# 获取第1级提示
python ../../learn.py --hint --question A1 --hint-level 1

# 获取第2级提示
python ../../learn.py --hint --question A1 --hint-level 2

# 获取第3级提示（接近答案）
python ../../learn.py --hint --question A1 --hint-level 3
```

#### 5️⃣ 查看答案

```bash
# 对比你的代码和答案
diff set_A_blank.py set_A_answers.py

# 或直接查看答案
cat set_A_answers.py
```

#### 6️⃣ 理解注释

```bash
# 查看详细注释版本
cat set_A_answers_annotated.py
```

这个版本包含：
- 详细的代码注释
- 知识点解释
- 最佳实践说明
- 常见陷阱提醒

---

## 🎯 第一天目标

完成第1阶段的第一套题（Set A）：

- [ ] 查看并理解题目要求
- [ ] 完成所有函数的实现
- [ ] 通过所有测试
- [ ] 阅读答案注释版
- [ ] 理解每个知识点

**预计时间**：1-2 小时

---

## 📊 追踪进度

### 查看总体进度

```bash
make progress
```

### 查看详细统计

```bash
make stats
```

你会看到按难度和主题分类的统计：

```
按难度分类：
  ⭐ 简单：0 题
  ⭐⭐ 中等：0 题
  ⭐⭐⭐ 困难：0 题
  ⭐⭐⭐⭐ 专家：0 题

按主题分类：
  基础语法：0/2 题
  数据处理：0/2 题
  算法：0/3 题
  ...
```

---

## 🛠️ 常用命令

```bash
# 环境管理
make setup              # 初始化项目
make install            # 安装依赖
make clean              # 清理临时文件

# 学习工具
make learn LEVEL=01     # 学习指定阶段
make progress           # 查看进度
make stats              # 查看统计

# 测试运行
make test               # 运行所有测试
make answers            # 运行答案版
make blank              # 运行空白版

# 帮助
make help               # 查看所有命令
```

---

## 📖 更多资源

- **[学习路径](LEARNING_PATH.md)** - 完整的8阶段学习指南
- **[快速开始](QUICK_START.md)** - 详细的快速开始指南
- **[知识图谱](KNOWLEDGE_MAP.md)** - 知识点关联图谱
- **[常见问题](FAQ.md)** - 22个常见问题解答
- **[改造总结](PROJECT_SUMMARY.md)** - 项目改造详情

---

## 💡 学习建议

### 对于初学者

1. **按顺序学习** - 从第1阶段开始，不要跳过
2. **动手实践** - 不要只看答案，一定要自己写
3. **理解原理** - 看注释版，理解为什么这样写
4. **每天坚持** - 每天1-2小时，比一次学很久效果好

### 对于有经验者

1. **快速浏览** - 先看题目，熟悉的可以跳过
2. **重点突破** - 专注于不熟悉的主题
3. **深入理解** - 看注释版，学习最佳实践
4. **举一反三** - 尝试优化代码，探索不同解法

### 对于面试准备

1. **时间限制** - 给自己设定时间限制（如30分钟/题）
2. **模拟环境** - 不看答案，不查资料
3. **总结归纳** - 整理常见模式和技巧
4. **反复练习** - 重要的题目多做几遍

---

## ❓ 遇到问题？

1. **查看 [FAQ](FAQ.md)** - 22个常见问题解答
2. **查看注释版** - `set_*_answers_annotated.py`
3. **使用提示系统** - `python learn.py --hint --question A1`
4. **查看知识图谱** - 了解知识点关联

---

## 🎉 准备好了吗？

现在就开始你的 Python 学习之旅吧！

```bash
make setup && make learn
```

祝学习愉快！🚀

