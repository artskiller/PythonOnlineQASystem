# 🛠️ 工具脚本

这个目录包含了项目的所有工具脚本，用于辅助学习和练习。

---

## 📋 工具列表

### 1. **learn.py** - 交互式学习工具

提供分阶段的交互式学习体验。

**使用方法**：
```bash
# 从根目录运行
python tools/learn.py --level 01

# 或使用Makefile
make learn LEVEL=01
```

**功能**：
- ✅ 8个学习阶段
- ✅ 交互式练习
- ✅ 实时反馈
- ✅ 进度追踪

**参数**：
- `--level` - 指定学习阶段（01-08）

---

### 2. **progress.py** - 进度追踪工具

查看和管理学习进度。

**使用方法**：
```bash
# 查看进度
python tools/progress.py --show

# 查看详细统计
python tools/progress.py --stats

# 或使用Makefile
make progress
make stats
```

**功能**：
- ✅ 进度可视化
- ✅ 完成度统计
- ✅ 学习时间追踪
- ✅ 成绩分析

**参数**：
- `--show` - 显示进度概览
- `--stats` - 显示详细统计
- `--reset` - 重置进度（谨慎使用）

---

### 3. **interview_simulator.py** - 面试模拟器

模拟真实的面试环境，进行限时练习。

**使用方法**：
```bash
# 标准2小时模拟面试
python tools/interview_simulator.py --duration 120

# 侧重AI技能
python tools/interview_simulator.py --duration 120 --focus ai

# 侧重财税业务
python tools/interview_simulator.py --duration 120 --focus tax

# 指定难度
python tools/interview_simulator.py --difficulty medium
```

**功能**：
- ✅ 限时练习
- ✅ 自动评分
- ✅ 详细报告
- ✅ 主题筛选

**参数**：
- `--duration` - 时长（分钟），默认120
- `--focus` - 侧重点：ai/tax/all
- `--difficulty` - 难度：easy/medium/hard
- `--sets` - 指定题目集（逗号分隔）

**示例**：
```bash
# AI工程师面试模拟（90分钟）
python tools/interview_simulator.py --duration 90 --focus ai --difficulty hard

# 财税业务面试模拟
python tools/interview_simulator.py --duration 120 --focus tax

# 自定义题目集
python tools/interview_simulator.py --sets ML1,NLP1,OCR1 --duration 120
```

---

## 🚀 快速开始

### 新手学习流程

```bash
# 1. 开始第一阶段学习
make learn LEVEL=01

# 2. 查看学习进度
make progress

# 3. 继续下一阶段
make learn LEVEL=02
```

### 面试准备流程

```bash
# 1. 先完成基础学习
make learn LEVEL=01
make learn LEVEL=02

# 2. 进行AI专项练习
python tools/interview_simulator.py --focus ai --duration 90

# 3. 完整模拟面试
python tools/interview_simulator.py --duration 120
```

---

## 📊 工具对比

| 工具 | 用途 | 适合场景 | 时间投入 |
|------|------|----------|----------|
| learn.py | 系统学习 | 新手入门、知识巩固 | 每阶段1-2小时 |
| progress.py | 进度管理 | 查看学习情况 | 1-2分钟 |
| interview_simulator.py | 面试准备 | 模拟真实面试 | 1-2小时 |

---

## 🔧 开发说明

### 添加新工具

1. 在 `tools/` 目录创建新的Python文件
2. 添加命令行参数解析
3. 在 `Makefile` 中添加快捷命令
4. 更新本README文档

### 工具依赖

所有工具依赖项目根目录的 `requirements.txt`：

```bash
pip install -r requirements.txt
```

---

## 📝 注意事项

1. **工作目录**：所有工具都应该从项目根目录运行
2. **Python版本**：需要Python 3.8+
3. **依赖安装**：运行前确保已安装依赖
4. **进度文件**：`.learning_progress.json` 保存在项目根目录

---

**返回 [项目主页](../README.md)**

