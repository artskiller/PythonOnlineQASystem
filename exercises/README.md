# 📚 练习题目录

本目录按学习阶段组织了所有练习题。每个阶段包含多套题目，每套题目有三个版本：

- **blank.py** - 空白版（填空练习）
- **answers.py** - 答案版（参考实现）
- **answers_annotated.py** - 注释版（详细解释）

## 📂 目录结构

```
exercises/
├── 01_basics/          # 第1阶段：基础入门
│   ├── set_A_*.py     # 基础与标准库
│   └── set_K_*.py     # 基础综合
│
├── 02_data/           # 第2阶段：数据处理
│   ├── set_B_*.py     # pandas 基础
│   └── set_G_*.py     # pandas 进阶
│
├── 03_algorithm/      # 第3阶段：算法思维
│   ├── set_C_*.py     # 算法与 Pythonic
│   ├── set_I_*.py     # 算法进阶
│   └── set_O_*.py     # 算法实战
│
├── 04_concurrency/    # 第4阶段：并发编程
│   ├── set_D_*.py     # 并发与性能
│   ├── set_H_*.py     # 并发进阶
│   └── set_T_*.py     # 异步编排
│
├── 05_engineering/    # 第5阶段：工程实践
│   ├── set_L_*.py     # 调试与修复
│   ├── set_N_*.py     # 异常与上下文
│   ├── set_P_*.py     # 日志与可观测性
│   └── set_M_*.py     # 设计与文档
│
├── 06_business/       # 第6阶段：业务应用
│   ├── set_E_*.py     # 业务综合
│   ├── set_J_*.py     # 业务进阶
│   ├── set_F_*.py     # 文本与高精度
│   └── set_Q_*.py     # 脱敏与合规
│
├── 07_system/         # 第7阶段：系统设计
│   ├── set_R_*.py     # SQLite 与 SQL 安全
│   ├── set_S_*.py     # API 契约
│   ├── set_U_*.py     # Tracing 模拟
│   ├── set_V_*.py     # OCR 文本清洗
│   ├── set_W_*.py     # 批量导入流水线
│   ├── set_X_*.py     # 审计日志轮转
│   └── set_Y_*.py     # 简易规则引擎
│
└── 08_projects/       # 第8阶段：综合项目
    ├── set_Z_*.py     # 端到端小项目
    ├── set_AA_*.py    # 端到端·并发版
    └── set_AB_*.py    # 端到端·HTTP 服务
```

## 🚀 使用方法

### 方式 1：按阶段学习

```bash
# 进入第1阶段目录
cd exercises/01_basics

# 编辑空白版
vim set_A_blank.py

# 运行测试
python set_A_blank.py

# 对比答案
diff set_A_blank.py set_A_answers.py

# 查看详细注释
cat set_A_answers_annotated.py
```

### 方式 2：使用学习工具

```bash
# 交互式学习
python learn.py --level 01

# 查看进度
python progress.py --show
```

### 方式 3：直接运行原始文件

```bash
# 所有原始文件仍在 interview_exercises/ 目录
python interview_exercises/set_A_blank.py
```

## 📖 学习建议

1. **按顺序学习** - 从 01 到 08，循序渐进
2. **独立完成** - 先不看答案，尝试独立解决
3. **对比学习** - 完成后对比三个版本
4. **举一反三** - 修改测试用例，测试边界情况
5. **定期复习** - 每周回顾已完成的题目

## 🔗 相关文档

- [学习路径](../LEARNING_PATH.md) - 详细的学习计划
- [快速开始](../QUICK_START.md) - 快速上手指南
- [知识图谱](../KNOWLEDGE_MAP.md) - 知识点关联
- [常见问题](../FAQ.md) - 疑难解答

---

**注意**：本目录中的文件是指向 `interview_exercises/` 的符号链接，方便按阶段组织。原始文件保持不变。
