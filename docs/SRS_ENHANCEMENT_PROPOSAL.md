# SRS需求文档功能补充建议

**文档版本**: V1.0  
**编写日期**: 2025-11-07  
**目标版本**: SRS V4.0

---

## 📋 补充需求清单

### 第4.8章 协作与社交功能

#### 4.8.1 题目讨论区 [P0]

**需求ID**: FR-CL-001  
**优先级**: 🔥🔥🔥 高  
**用户故事**: 作为学生，我希望能在题目下方看到其他同学的讨论，学习不同的解题思路。

**功能描述**:
1. 每道题目下方有讨论区
2. 支持发表评论和回复
3. 支持Markdown格式
4. 支持代码高亮
5. 支持点赞和排序（按热度/时间）
6. 支持@提及用户
7. 支持举报不当内容

**界面设计**:
```
┌─────────────────────────────────────────┐
│ 💬 讨论区 (23条讨论)                     │
├─────────────────────────────────────────┤
│ 🔥 热门讨论                              │
│                                         │
│ 👤 张三  ⭐⭐⭐  2小时前  👍 15          │
│ 我用了切片的方法，代码很简洁：           │
│ ```python                               │
│ return s[::-1]                          │
│ ```                                     │
│ [回复(3)] [点赞] [举报]                 │
│                                         │
│   └─ 👤 李四  1小时前  👍 5             │
│      这个方法很巧妙！我之前用的是循环    │
│      [回复] [点赞]                      │
│                                         │
│ 👤 王五  ⭐  3小时前  👍 8               │
│ 请问为什么我的代码超时了？               │
│ [回复(2)] [点赞] [举报]                 │
│                                         │
│ [发表讨论...]                            │
└─────────────────────────────────────────┘
```

**数据模型**:
```sql
CREATE TABLE discussions (
    id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    parent_id INTEGER,  -- 回复的评论ID
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_id) REFERENCES discussions(id)
);

CREATE TABLE discussion_likes (
    id INTEGER PRIMARY KEY,
    discussion_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP,
    UNIQUE(discussion_id, user_id),
    FOREIGN KEY (discussion_id) REFERENCES discussions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**验收标准**:
- [ ] 支持发表和回复评论
- [ ] 支持Markdown和代码高亮
- [ ] 支持点赞和排序
- [ ] 支持@提及和通知
- [ ] 支持举报和审核

---

#### 4.8.2 问答社区 [P1]

**需求ID**: FR-CL-002  
**优先级**: 🔥🔥 中  
**用户故事**: 作为学生，我希望能在社区提问，获得老师和同学的帮助。

**功能描述**:
1. 独立的问答社区（类似Stack Overflow）
2. 支持提问和回答
3. 支持采纳最佳答案
4. 支持问题标签
5. 支持问题搜索
6. 支持问题关注
7. 积分奖励机制

**问题分类**:
- Python基础
- 数据结构
- 算法
- 项目实战
- 工具使用
- 其他

**积分规则**:
- 提问: -5分（防止灌水）
- 回答被采纳: +20分
- 回答被点赞: +2分/次
- 问题被点赞: +5分/次

**验收标准**:
- [ ] 支持提问和回答
- [ ] 支持采纳最佳答案
- [ ] 支持标签和搜索
- [ ] 积分奖励正确

---

#### 4.8.3 学习小组 [P1]

**需求ID**: FR-CL-003  
**优先级**: 🔥🔥 中  
**用户故事**: 作为学生，我希望能加入学习小组，和志同道合的同学一起学习。

**功能描述**:
1. 创建和加入学习小组
2. 小组讨论区
3. 小组学习计划
4. 小组排行榜
5. 小组活动（打卡、挑战）

**小组类型**:
- 公开小组（任何人可加入）
- 私密小组（需要审批）
- 班级小组（教师创建）

**验收标准**:
- [ ] 支持创建和加入小组
- [ ] 小组功能完整
- [ ] 小组数据统计准确

---

### 第4.9章 学习笔记系统

#### 4.9.1 题目笔记 [P0]

**需求ID**: FR-NT-001  
**优先级**: 🔥🔥🔥 高  
**用户故事**: 作为学生，我希望能在做题时记录笔记，方便日后复习。

**功能描述**:
1. 每道题目可以记笔记
2. 支持Markdown编辑
3. 支持代码高亮
4. 支持图片上传
5. 支持笔记版本历史
6. 支持笔记导出

**界面设计**:
```
┌─────────────────────────────────────────┐
│ 📝 我的笔记                              │
├─────────────────────────────────────────┤
│ [编辑] [预览] [历史] [导出]              │
│                                         │
│ ## 解题思路                              │
│                                         │
│ 这道题考察字符串切片的使用：             │
│ 1. Python的切片语法 `s[::-1]`           │
│ 2. 步长为-1表示反向                     │
│                                         │
│ ## 知识点                                │
│ - 字符串切片                             │
│ - 步长参数                               │
│                                         │
│ ## 易错点                                │
│ ⚠️ 注意空字符串的处理                    │
│                                         │
│ 最后编辑: 2024-01-15 14:30              │
└─────────────────────────────────────────┘
```

**数据模型**:
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(user_id, question_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE note_versions (
    id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES notes(id)
);
```

**验收标准**:
- [ ] 支持Markdown编辑和预览
- [ ] 支持代码高亮
- [ ] 支持图片上传
- [ ] 支持版本历史
- [ ] 支持导出（Markdown/PDF）

---

#### 4.9.2 知识点笔记 [P1]

**需求ID**: FR-NT-002
**优先级**: 🔥🔥 中
**用户故事**: 作为学生，我希望能整理知识点笔记，构建自己的知识体系。

**功能描述**:
1. 创建知识点笔记
2. 笔记分类和标签
3. 笔记关联题目
4. 笔记搜索
5. 笔记分享（可选）

**验收标准**:
- [ ] 支持创建和编辑知识点笔记
- [ ] 支持分类和标签
- [ ] 支持关联题目
- [ ] 支持搜索

---

#### 4.9.3 笔记搜索 [P1]

**需求ID**: FR-NT-003
**优先级**: 🔥🔥 中
**用户故事**: 作为学生，我希望能快速搜索我的笔记，找到需要的内容。

**功能描述**:
1. 全文搜索
2. 按标签搜索
3. 按题目搜索
4. 按时间搜索
5. 搜索结果高亮

**验收标准**:
- [ ] 搜索速度<1秒
- [ ] 搜索结果准确
- [ ] 支持高亮显示

---

### 第4.10章 错题本系统

#### 4.10.1 错题自动收集 [P0]

**需求ID**: FR-WB-001
**优先级**: 🔥🔥🔥 高
**用户故事**: 作为学生，我希望系统能自动收集我的错题，方便我针对性复习。

**功能描述**:
1. 自动识别错题（得分<60分）
2. 错题分类（按知识点）
3. 错题统计
4. 错题标签

**错题分类**:
- 完全不会（得分0-20分）
- 部分理解（得分21-40分）
- 粗心错误（得分41-59分）

**界面设计**:
```
┌─────────────────────────────────────────┐
│ 📕 我的错题本 (共23道)                   │
├─────────────────────────────────────────┤
│ 📊 错题统计                              │
│ 字符串操作: 5道  列表操作: 8道           │
│ 算法思维: 10道                           │
│                                         │
│ 🔍 筛选: [全部▼] [知识点▼] [难度▼]      │
│                                         │
│ ❌ STR001 字符串反转  ⭐⭐              │
│    错误次数: 2次  最后错误: 2天前        │
│    薄弱点: 字符串切片                    │
│    [重做] [查看笔记] [移出错题本]        │
│                                         │
│ ❌ LIST003 列表去重  ⭐⭐⭐             │
│    错误次数: 1次  最后错误: 5天前        │
│    薄弱点: 集合操作                      │
│    [重做] [查看笔记] [移出错题本]        │
└─────────────────────────────────────────┘
```

**数据模型**:
```sql
CREATE TABLE wrong_questions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    error_count INTEGER DEFAULT 1,
    last_error_at TIMESTAMP,
    mastery_level INTEGER DEFAULT 0,  -- 0-100
    is_mastered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    UNIQUE(user_id, question_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
```

**验收标准**:
- [ ] 自动识别错题
- [ ] 错题分类准确
- [ ] 错题统计正确

---

#### 4.10.2 错题重做 [P0]

**需求ID**: FR-WB-002
**优先级**: 🔥🔥🔥 高
**用户故事**: 作为学生，我希望能重做错题，巩固薄弱知识点。

**功能描述**:
1. 一键重做错题
2. 错题重做记录
3. 掌握度评估
4. 自动移出错题本（连续3次全对）

**掌握度评估**:
- 第1次重做通过: 掌握度+30%
- 第2次重做通过: 掌握度+30%
- 第3次重做通过: 掌握度+40%，移出错题本

**验收标准**:
- [ ] 支持重做错题
- [ ] 掌握度评估准确
- [ ] 自动移出逻辑正确

---

#### 4.10.3 错题分析 [P1]

**需求ID**: FR-WB-003
**优先级**: 🔥🔥 中
**用户故事**: 作为学生，我希望看到错题分析，了解我的薄弱环节。

**功能描述**:
1. 错题知识点分布
2. 错题难度分布
3. 错题趋势分析
4. 薄弱点识别

**分析报告**:
```
📊 错题分析报告

知识点分布:
字符串操作  ████████░░ 40%
列表操作    ██████████ 50%
算法思维    ████░░░░░░ 20%

难度分布:
⭐      ██░░░░░░░░ 10%
⭐⭐    ████████░░ 40%
⭐⭐⭐  ██████████ 50%

薄弱点TOP3:
1. 列表推导式 (8道错题)
2. 字符串切片 (5道错题)
3. 递归算法 (4道错题)

建议:
💡 重点复习列表推导式相关知识
💡 加强字符串切片练习
💡 学习递归算法的基本思想
```

**验收标准**:
- [ ] 分析数据准确
- [ ] 可视化清晰
- [ ] 建议有参考价值

---

### 第4.11章 教师功能增强

#### 4.11.1 班级管理 [P0]

**需求ID**: FR-TC-001
**优先级**: 🔥🔥🔥 高
**用户故事**: 作为教师，我希望能创建和管理班级，组织学生学习。

**功能描述**:
1. 创建班级
2. 添加/移除学生
3. 班级公告
4. 班级数据统计

**界面设计**:
```
┌─────────────────────────────────────────┐
│ 👥 我的班级                              │
├─────────────────────────────────────────┤
│ 📚 Python基础班 (45人)                   │
│    创建时间: 2024-01-01                  │
│    [查看详情] [发布公告] [布置作业]      │
│                                         │
│ 📊 班级统计                              │
│ 平均学习时长: 12小时/周                  │
│ 平均完成题数: 15道/周                    │
│ 平均通过率: 78%                          │
│                                         │
│ 👤 学生列表 (45人)                       │
│ [搜索学生...]                            │
│                                         │
│ 1. 张三  学习时长: 20h  完成: 25题  ⭐⭐⭐│
│ 2. 李四  学习时长: 15h  完成: 18题  ⭐⭐  │
│ 3. 王五  学习时长: 8h   完成: 10题  ⭐   │
│    ⚠️ 学习进度落后                       │
└─────────────────────────────────────────┘
```

**数据模型**:
```sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    teacher_id INTEGER NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

CREATE TABLE class_members (
    id INTEGER PRIMARY KEY,
    class_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at TIMESTAMP,
    UNIQUE(class_id, user_id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE class_announcements (
    id INTEGER PRIMARY KEY,
    class_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id)
);
```

**验收标准**:
- [ ] 支持创建和管理班级
- [ ] 支持添加/移除学生
- [ ] 支持发布公告
- [ ] 班级统计准确

---

#### 4.11.2 作业系统 [P0]

**需求ID**: FR-TC-002
**优先级**: 🔥🔥🔥 高
**用户故事**: 作为教师，我希望能布置作业，并查看学生完成情况。

**功能描述**:
1. 创建作业（选择题目）
2. 设置截止时间
3. 自动批改
4. 作业统计分析
5. 学生提交查看

**作业类型**:
- 练习作业（不计分）
- 考核作业（计入成绩）
- 挑战作业（额外加分）

**界面设计**:
```
┌─────────────────────────────────────────┐
│ 📝 创建作业                              │
├─────────────────────────────────────────┤
│ 作业名称: [第一周练习作业_________]      │
│ 作业类型: [练习作业 ▼]                   │
│ 截止时间: [2024-01-20 23:59]            │
│ 目标班级: [Python基础班 ▼]              │
│                                         │
│ 📚 选择题目 (已选5道)                    │
│ [+ 添加题目]                             │
│                                         │
│ ✓ STR001 字符串反转  ⭐⭐               │
│ ✓ LIST002 列表去重  ⭐⭐⭐              │
│ ✓ DICT001 字典操作  ⭐⭐                │
│                                         │
│ 💯 评分设置                              │
│ 总分: 100分                              │
│ 及格分: 60分                             │
│ 允许重做: ☑️                             │
│ 显示答案: ☑️ (提交后)                    │
│                                         │
│ [发布作业] [保存草稿] [取消]             │
└─────────────────────────────────────────┘
```

**数据模型**:
```sql
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    class_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,  -- practice/exam/challenge
    deadline TIMESTAMP,
    total_score INTEGER DEFAULT 100,
    pass_score INTEGER DEFAULT 60,
    allow_retry BOOLEAN DEFAULT TRUE,
    show_answer BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

CREATE TABLE assignment_questions (
    id INTEGER PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    order_num INTEGER NOT NULL,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE assignment_submissions (
    id INTEGER PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score INTEGER,
    status VARCHAR(20),  -- pending/submitted/graded
    submitted_at TIMESTAMP,
    UNIQUE(assignment_id, user_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**验收标准**:
- [ ] 支持创建和发布作业
- [ ] 支持自动批改
- [ ] 支持作业统计
- [ ] 支持查看学生提交

---

#### 4.11.3 学生数据查看 [P0]

**需求ID**: FR-TC-003
**优先级**: 🔥🔥🔥 高
**用户故事**: 作为教师，我希望能查看学生的详细学习数据，了解学生学习情况。

**功能描述**:
1. 查看学生学习时长
2. 查看学生完成题数
3. 查看学生通过率
4. 查看学生薄弱点
5. 学生对比分析

**学生详情页**:
```
┌─────────────────────────────────────────┐
│ 👤 张三 - 学习数据                       │
├─────────────────────────────────────────┤
│ 📊 学习概况                              │
│ 学习时长: 20小时  完成题数: 25道         │
│ 通过率: 85%  平均得分: 87分              │
│ 等级: ⭐⭐⭐  积分: 1250                │
│                                         │
│ 📈 学习趋势                              │
│ [折线图: 最近7天学习时长]                │
│                                         │
│ 💪 知识点掌握                            │
│ 字符串操作  ████████░░ 80%              │
│ 列表操作    ██████████ 95%              │
│ 算法思维    ████░░░░░░ 40%  ⚠️          │
│                                         │
│ ⚠️ 薄弱点                                │
│ 1. 递归算法 (通过率30%)                  │
│ 2. 动态规划 (通过率25%)                  │
│                                         │
│ 📝 最近提交 (5条)                        │
│ [查看全部提交]                           │
└─────────────────────────────────────────┘
```

**验收标准**:
- [ ] 数据展示完整
- [ ] 数据准确
- [ ] 可视化清晰

---

### 第4.12章 课程体系

#### 4.12.1 课程创建 [P1]

**需求ID**: FR-CR-001
**优先级**: 🔥🔥 中
**用户故事**: 作为教师，我希望能创建系统化的课程，而不仅仅是题目。

**功能描述**:
1. 创建课程
2. 添加课程章节
3. 章节内容编辑（Markdown）
4. 关联题目
5. 课程发布

**课程结构**:
```
课程: Python基础入门
├── 第1章: Python简介
│   ├── 1.1 Python是什么
│   ├── 1.2 Python的应用
│   └── 练习题: 3道
├── 第2章: 变量和数据类型
│   ├── 2.1 变量定义
│   ├── 2.2 数据类型
│   ├── 2.3 类型转换
│   └── 练习题: 5道
└── 第3章: 控制流
    ├── 3.1 if语句
    ├── 3.2 for循环
    ├── 3.3 while循环
    └── 练习题: 8道
```

**数据模型**:
```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty INTEGER,  -- 1-5
    estimated_hours INTEGER,
    teacher_id INTEGER NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

CREATE TABLE chapters (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,  -- Markdown
    order_num INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE chapter_questions (
    id INTEGER PRIMARY KEY,
    chapter_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    order_num INTEGER NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
```

**验收标准**:
- [ ] 支持创建课程
- [ ] 支持章节管理
- [ ] 支持Markdown编辑
- [ ] 支持关联题目

---

## 📊 实施优先级

### Phase 1: 核心协作功能 (1个月)

**目标**: 增强师生互动和学习体验

| 需求ID | 功能 | 优先级 | 工作量 |
|--------|------|--------|--------|
| FR-CL-001 | 题目讨论区 | P0 | 5天 |
| FR-NT-001 | 题目笔记 | P0 | 3天 |
| FR-WB-001 | 错题自动收集 | P0 | 3天 |
| FR-WB-002 | 错题重做 | P0 | 2天 |
| FR-TC-001 | 班级管理 | P0 | 5天 |
| FR-TC-002 | 作业系统 | P0 | 7天 |
| FR-TC-003 | 学生数据查看 | P0 | 3天 |

**总计**: 7个需求，28天

---

### Phase 2: 学习体系完善 (1个月)

**目标**: 构建完整的学习内容体系

| 需求ID | 功能 | 优先级 | 工作量 |
|--------|------|--------|--------|
| FR-CL-002 | 问答社区 | P1 | 7天 |
| FR-CL-003 | 学习小组 | P1 | 5天 |
| FR-NT-002 | 知识点笔记 | P1 | 3天 |
| FR-NT-003 | 笔记搜索 | P1 | 2天 |
| FR-WB-003 | 错题分析 | P1 | 3天 |
| FR-CR-001 | 课程创建 | P1 | 7天 |

**总计**: 6个需求，27天

---

## 🎯 总结

### 补充需求统计

- **新增需求**: 13个
- **P0需求**: 7个
- **P1需求**: 6个
- **预计工作量**: 55天

### 核心改进点

1. ✅ **协作互动**: 讨论区、问答社区、学习小组
2. ✅ **学习工具**: 笔记系统、错题本
3. ✅ **教学管理**: 班级、作业、学生数据
4. ✅ **内容体系**: 课程、章节、学习路径

### 预期效果

- **用户活跃度**: 提升50%（通过协作功能）
- **学习效果**: 提升30%（通过错题本和笔记）
- **教师满意度**: 提升60%（通过教学管理功能）
- **平台粘性**: 提升40%（通过课程体系）

---

**文档结束**


