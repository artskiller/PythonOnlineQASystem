# 详细设计说明书 (DDS)
# Detailed Design Specification

**项目名称**: pythonLearn - Python交互式学习平台  
**文档版本**: V2.0  
**编写日期**: 2025-11-07  
**文档状态**: 正式版  
**密级**: 内部公开

---

## 文档修订历史

| 版本 | 日期 | 修订人 | 修订内容 | 审核人 |
|------|------|--------|---------|--------|
| V1.0 | 2025-11-07 | 开发团队 | 初始版本 | - |
| V2.0 | 2025-11-07 | 开发团队 | 添加V2.0架构设计 | - |
| V3.0 | 2025-11-07 | 开发团队 | 结合商用系统经验完善设计 | - |

---

## 目录

1. [引言](#1-引言)
2. [系统架构设计](#2-系统架构设计)
3. [模块设计](#3-模块设计)
4. [数据库设计](#4-数据库设计)
5. [接口设计](#5-接口设计)
6. [安全设计](#6-安全设计)
7. [性能设计](#7-性能设计)
8. [部署设计](#8-部署设计)
9. [运维设计](#9-运维设计)

---

## 1. 引言

### 1.1 目的

本文档详细描述pythonLearn Python交互式学习平台V2.0的详细设计，包括系统架构、模块设计、数据库设计、接口设计等。本文档面向：

- **架构师**: 了解系统架构
- **开发人员**: 作为开发依据
- **测试人员**: 了解系统设计
- **运维人员**: 了解部署架构

### 1.2 范围

本文档涵盖pythonLearn V2.0的所有技术设计细节，包括：

- 系统架构（前端、后端、数据库、容器）
- 模块设计（6大功能模块）
- 数据库设计（15张表）
- API接口设计（RESTful API）
- 安全设计（认证、授权、沙箱）
- 部署设计（Docker、单机/局域网）

### 1.3 参考文档

- [软件需求规格说明书](SRS_SOFTWARE_REQUIREMENTS_SPECIFICATION.md)
- [架构演进规划V2](ARCHITECTURE_EVOLUTION_V2.md)
- [优化方案文档](OPTIMIZATION_PLAN.md)

---

## 2. 系统架构设计

### 2.1 总体架构

pythonLearn V2.0采用**前后端分离**的架构，使用**Docker容器化**部署。

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Vue.js 3   │  │    Pinia     │  │  CodeMirror  │      │
│  │  (前端框架)  │  │  (状态管理)  │  │  (编辑器)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Nginx (反向代理)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  静态文件    │  │  API代理     │  │  负载均衡    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  API层       │  │  业务逻辑层  │  │  数据访问层  │      │
│  │  (routes)    │  │  (services)  │  │  (models)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   SQLite     │  │    Docker    │  │   文件系统   │
│   数据库     │  │   代码沙箱   │  │   题目文件   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 技术栈

#### 2.2.1 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue.js** | 3.3+ | 前端框架 |
| **Vite** | 4.0+ | 构建工具 |
| **Pinia** | 2.1+ | 状态管理 |
| **Vue Router** | 4.2+ | 路由管理 |
| **Axios** | 1.4+ | HTTP客户端 |
| **CodeMirror** | 6.0+ | 代码编辑器 |
| **Chart.js** | 4.0+ | 图表库 |
| **Tailwind CSS** | 3.3+ | CSS框架 |

#### 2.2.2 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 编程语言 |
| **Flask** | 2.3+ | Web框架 |
| **SQLAlchemy** | 2.0+ | ORM |
| **Flask-JWT-Extended** | 4.5+ | JWT认证 |
| **Flask-CORS** | 4.0+ | 跨域支持 |
| **PyYAML** | 6.0+ | YAML解析 |
| **Docker SDK** | 6.1+ | Docker API |
| **Gunicorn** | 21.0+ | WSGI服务器 |

#### 2.2.3 数据库和存储

| 技术 | 版本 | 用途 |
|------|------|------|
| **SQLite** | 3.35+ | 关系数据库 |
| **文件系统** | - | 题目文件存储 |

#### 2.2.4 容器和部署

| 技术 | 版本 | 用途 |
|------|------|------|
| **Docker** | 20.10+ | 容器引擎 |
| **Docker Compose** | 2.0+ | 容器编排 |
| **Nginx** | 1.21+ | 反向代理 |

### 2.3 架构分层

#### 2.3.1 前端分层

```
前端架构
├── 视图层 (Views)
│   ├── 页面组件
│   └── 布局组件
│
├── 组件层 (Components)
│   ├── 业务组件
│   └── 通用组件
│
├── 状态层 (Stores)
│   ├── 用户状态
│   ├── 题目状态
│   └── 学习状态
│
├── 服务层 (Services)
│   ├── API服务
│   └── 工具服务
│
└── 路由层 (Router)
    ├── 路由配置
    └── 路由守卫
```

#### 2.3.2 后端分层

```
后端架构
├── API层 (Routes)
│   ├── 认证路由
│   ├── 题目路由
│   ├── 提交路由
│   └── 用户路由
│
├── 业务逻辑层 (Services)
│   ├── 用户服务
│   ├── 题目服务
│   ├── 执行服务
│   └── 推荐服务
│
├── 数据访问层 (Models)
│   ├── ORM模型
│   └── 数据库操作
│
└── 工具层 (Utils)
    ├── 认证工具
    ├── 验证工具
    └── 辅助工具
```

### 2.4 数据流

#### 2.4.1 用户登录流程

```
用户 → 前端 → 后端 → 数据库
 │      │      │      │
 │      │      │      └─ 验证用户名密码
 │      │      └─ 生成JWT Token
 │      └─ 保存Token到localStorage
 └─ 跳转到首页
```

#### 2.4.2 代码执行流程

```
用户 → 前端 → 后端 → Docker → 后端 → 前端 → 用户
 │      │      │      │      │      │      │
 │      │      │      │      │      │      └─ 显示结果
 │      │      │      │      │      └─ 返回执行结果
 │      │      │      │      └─ 收集结果
 │      │      │      └─ 执行代码
 │      │      └─ 创建Docker容器
 │      └─ 发送代码
 └─ 点击运行
```

---

## 3. 模块设计

### 3.1 前端模块设计

#### 3.1.1 目录结构

```
web-frontend/
├── public/                 # 静态资源
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── assets/            # 资源文件
│   │   ├── images/
│   │   └── styles/
│   │
│   ├── components/        # 组件
│   │   ├── common/        # 通用组件
│   │   │   ├── Button.vue
│   │   │   ├── Input.vue
│   │   │   └── Modal.vue
│   │   │
│   │   ├── editor/        # 编辑器组件
│   │   │   ├── CodeEditor.vue
│   │   │   ├── HintPanel.vue
│   │   │   └── TestResults.vue
│   │   │
│   │   └── learning/      # 学习组件
│   │       ├── ProgressBar.vue
│   │       ├── QuestionCard.vue
│   │       └── LearningPath.vue
│   │
│   ├── views/             # 页面
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── QuestionList.vue
│   │   ├── QuestionDetail.vue
│   │   ├── Profile.vue
│   │   └── Dashboard.vue
│   │
│   ├── stores/            # 状态管理
│   │   ├── user.js
│   │   ├── question.js
│   │   └── learning.js
│   │
│   ├── services/          # API服务
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── question.js
│   │
│   ├── router/            # 路由
│   │   └── index.js
│   │
│   ├── utils/             # 工具函数
│   │   ├── request.js
│   │   └── helpers.js
│   │
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
│
├── package.json
└── vite.config.js
```

#### 3.1.2 核心组件设计

**CodeEditor.vue - 代码编辑器组件**

```vue
<template>
  <div class="code-editor">
    <div class="editor-header">
      <h3>{{ question.title }}</h3>
      <div class="actions">
        <button @click="runCode">运行</button>
        <button @click="resetCode">重置</button>
        <button @click="showHint">提示</button>
      </div>
    </div>

    <div class="editor-body">
      <codemirror
        v-model="code"
        :options="editorOptions"
        @change="onCodeChange"
      />
    </div>

    <div class="editor-footer">
      <TestResults :results="testResults" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuestionStore } from '@/stores/question'

const questionStore = useQuestionStore()
const code = ref('')
const testResults = ref([])

const editorOptions = {
  mode: 'python',
  theme: 'monokai',
  lineNumbers: true,
  autoCloseBrackets: true,
  matchBrackets: true
}

const runCode = async () => {
  const results = await questionStore.executeCode(code.value)
  testResults.value = results
}

const resetCode = () => {
  code.value = questionStore.currentQuestion.template
}

const showHint = async (level) => {
  await questionStore.getHint(level)
}
</script>
```

**QuestionCard.vue - 题目卡片组件**

```vue
<template>
  <div class="question-card" @click="goToQuestion">
    <div class="card-header">
      <h4>{{ question.title }}</h4>
      <span class="difficulty">{{ getDifficulty(question.difficulty) }}</span>
    </div>

    <div class="card-body">
      <p class="description">{{ question.description }}</p>
      <div class="meta">
        <span class="category">{{ question.category }}</span>
        <span class="time">{{ question.estimated_time }}分钟</span>
      </div>
    </div>

    <div class="card-footer">
      <div class="tags">
        <span v-for="tag in question.tags" :key="tag" class="tag">
          {{ tag }}
        </span>
      </div>
      <div class="status">
        <span v-if="question.completed" class="completed">✓ 已完成</span>
        <span v-else class="pending">待完成</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  question: Object
})

const router = useRouter()

const getDifficulty = (level) => {
  return '⭐'.repeat(level)
}

const goToQuestion = () => {
  router.push(`/questions/${props.question.id}`)
}
</script>
```

### 3.2 后端模块设计

#### 3.2.1 目录结构

```
backend/
├── app/
│   ├── __init__.py        # 应用初始化
│   │
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── submission.py
│   │   └── achievement.py
│   │
│   ├── routes/            # 路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── questions.py
│   │   ├── submissions.py
│   │   └── users.py
│   │
│   ├── services/          # 业务逻辑
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── question_service.py
│   │   ├── executor_service.py
│   │   └── recommender_service.py
│   │
│   ├── utils/             # 工具函数
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   │
│   └── config.py          # 配置文件
│
├── migrations/            # 数据库迁移
├── tests/                 # 测试文件
├── requirements.txt       # 依赖
└── run.py                 # 启动文件
```

#### 3.2.2 核心模块设计

**auth_service.py - 认证服务**

```python
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

class AuthService:
    @staticmethod
    def register(username, email, password):
        """用户注册"""
        # 检查用户是否存在
        if User.query.filter_by(username=username).first():
            raise ValueError('用户名已存在')

        if User.query.filter_by(email=email).first():
            raise ValueError('邮箱已存在')

        # 创建用户
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def login(username, password):
        """用户登录"""
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError('用户名或密码错误')

        # 生成JWT Token
        access_token = create_access_token(identity=user.id)

        return {
            'user': user.to_dict(),
            'access_token': access_token
        }

    @staticmethod
    def get_current_user(user_id):
        """获取当前用户"""
        return User.query.get_or_404(user_id)
```

**executor_service.py - 代码执行服务**

```python
import docker
import json
import tempfile
import os
from typing import List, Dict

class ExecutorService:
    def __init__(self):
        self.client = docker.from_env()
        self.image = 'python:3.9-alpine'

    def execute(self, code: str, test_cases: List[Dict], timeout: int = 5) -> Dict:
        """执行代码"""
        results = []

        for test_case in test_cases:
            try:
                result = self._run_test_case(code, test_case, timeout)
                results.append(result)
            except Exception as e:
                results.append({
                    'test_case': test_case,
                    'error': str(e),
                    'passed': False
                })

        # 计算得分
        total = len(results)
        passed = sum(1 for r in results if r.get('passed', False))
        score = (passed / total * 100) if total > 0 else 0

        return {
            'success': score == 100,
            'score': score,
            'passed': passed,
            'total': total,
            'results': results
        }

    def _run_test_case(self, code: str, test_case: Dict, timeout: int) -> Dict:
        """运行单个测试用例"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as f:
            # 写入代码
            f.write(code)
            f.write('\n\n')

            # 写入测试
            f.write('# Test case\n')
            f.write(f'result = {test_case["function_call"]}\n')
            f.write('print(json.dumps(result))\n')

            temp_file = f.name

        try:
            # 运行容器
            output = self.client.containers.run(
                self.image,
                f'python /code/test.py',
                volumes={
                    temp_file: {
                        'bind': '/code/test.py',
                        'mode': 'ro'
                    }
                },
                mem_limit='128m',
                cpu_period=100000,
                cpu_quota=50000,
                network_disabled=True,
                timeout=timeout,
                remove=True
            )

            # 解析输出
            actual = json.loads(output.decode().strip())
            expected = test_case['expected']
            passed = actual == expected

            return {
                'test_case': test_case,
                'actual': actual,
                'expected': expected,
                'passed': passed
            }

        finally:
            # 删除临时文件
            os.unlink(temp_file)
```

**recommender_service.py - 推荐服务**

```python
from app.models.question import Question
from app.models.submission import Submission
from app.models.knowledge_point import KnowledgePoint
from sqlalchemy import func

class RecommenderService:
    @staticmethod
    def recommend_questions(user_id: int, count: int = 5) -> List[Question]:
        """推荐题目"""
        # 1. 构建用户画像
        profile = RecommenderService._build_user_profile(user_id)

        # 2. 找出弱项知识点
        weak_points = [
            kp for kp, score in profile['knowledge_scores'].items()
            if score < 0.7
        ]

        # 3. 找出相关题目
        candidates = Question.query.join(
            Question.knowledge_points
        ).filter(
            KnowledgePoint.name.in_(weak_points)
        ).all()

        # 4. 过滤已完成题目
        completed_ids = {
            s.question_id
            for s in Submission.query.filter_by(
                user_id=user_id,
                success=True
            ).all()
        }

        candidates = [
            q for q in candidates
            if q.id not in completed_ids
        ]

        # 5. 按难度排序
        candidates.sort(key=lambda q: q.difficulty)

        return candidates[:count]

    @staticmethod
    def _build_user_profile(user_id: int) -> Dict:
        """构建用户画像"""
        submissions = Submission.query.filter_by(
            user_id=user_id
        ).all()

        # 统计各知识点掌握情况
        knowledge_scores = {}

        for sub in submissions:
            for kp in sub.question.knowledge_points:
                if kp.name not in knowledge_scores:
                    knowledge_scores[kp.name] = []

                knowledge_scores[kp.name].append(
                    1.0 if sub.success else 0.0
                )

        # 计算平均分
        knowledge_scores = {
            k: sum(v) / len(v)
            for k, v in knowledge_scores.items()
        }

        return {
            'knowledge_scores': knowledge_scores,
            'total_submissions': len(submissions),
            'success_rate': sum(
                1 for s in submissions if s.success
            ) / len(submissions) if submissions else 0
        }
```

---

## 4. 数据库设计

### 4.1 ER图

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │  Question    │       │  Submission  │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│ username     │       │ title        │       │ user_id (FK) │
│ email        │       │ type         │       │ question_id  │
│ password_hash│       │ category     │       │ code         │
│ level        │       │ difficulty   │       │ result       │
│ points       │       │ description  │       │ success      │
│ created_at   │       │ template     │       │ score        │
└──────────────┘       │ solution     │       │ submitted_at │
       │               │ created_at   │       └──────────────┘
       │               └──────────────┘              │
       │                      │                      │
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌──────────────┐    ┌──────────────┐
            │ Achievement  │    │ KnowledgePoint│
            ├──────────────┤    ├──────────────┤
            │ id (PK)      │    │ id (PK)      │
            │ name         │    │ name         │
            │ description  │    │ category     │
            │ icon         │    │ description  │
            │ points       │    └──────────────┘
            └──────────────┘
```

### 4.2 表结构设计

#### 4.2.1 用户表 (users)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    level INTEGER DEFAULT 1,
    points INTEGER DEFAULT 0,
    avatar VARCHAR(200),
    bio TEXT,
    role VARCHAR(20) DEFAULT 'student',  -- student/teacher/admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,

    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

**字段说明**:
- `id`: 用户ID，主键，自增
- `username`: 用户名，唯一，3-20字符
- `email`: 邮箱，唯一
- `password_hash`: 密码哈希，BCrypt加密
- `level`: 用户等级，1-10
- `points`: 积分
- `avatar`: 头像URL
- `bio`: 个人简介
- `role`: 角色（学生/教师/管理员）
- `created_at`: 注册时间
- `last_login`: 最后登录时间

#### 4.2.2 题目表 (questions)

```sql
CREATE TABLE questions (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- coding/choice/judge/debug/sql/project
    category VARCHAR(50),
    difficulty INTEGER,  -- 1-5星
    estimated_time INTEGER,  -- 分钟
    description TEXT,
    template TEXT,
    solution TEXT,
    explanation TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,

    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    INDEX idx_type (type)
);
```

**字段说明**:
- `id`: 题目ID，主键，如"STR001"
- `title`: 题目标题
- `type`: 题目类型
- `category`: 分类（基础入门/数据处理等）
- `difficulty`: 难度（1-5星）
- `estimated_time`: 预计完成时间（分钟）
- `description`: 题目描述
- `template`: 代码模板
- `solution`: 参考答案
- `explanation`: 详细解释
- `created_by`: 创建者ID
- `created_at`: 创建时间
- `updated_at`: 更新时间

#### 4.2.3 测试用例表 (test_cases)

```sql
CREATE TABLE test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id VARCHAR(20) REFERENCES questions(id),
    input TEXT,
    expected_output TEXT,
    is_hidden BOOLEAN DEFAULT FALSE,
    weight REAL DEFAULT 1.0,
    order_num INTEGER,

    INDEX idx_question (question_id)
);
```

#### 4.2.4 提示表 (hints)

```sql
CREATE TABLE hints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id VARCHAR(20) REFERENCES questions(id),
    level INTEGER,  -- 1-3
    content TEXT,
    cost INTEGER DEFAULT 5,  -- 消耗积分

    INDEX idx_question_level (question_id, level)
);
```

#### 4.2.5 提交记录表 (submissions)

```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    question_id VARCHAR(20) REFERENCES questions(id),
    code TEXT NOT NULL,
    result TEXT,  -- JSON格式的执行结果
    success BOOLEAN,
    score REAL,
    execution_time REAL,  -- 秒
    memory_used REAL,  -- MB
    used_hints BOOLEAN DEFAULT FALSE,
    points_earned INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user (user_id),
    INDEX idx_question (question_id),
    INDEX idx_submitted_at (submitted_at)
);
```

#### 4.2.6 学习进度表 (progress)

```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    question_id VARCHAR(20) REFERENCES questions(id),
    status VARCHAR(20),  -- not_started/in_progress/completed
    code TEXT,  -- 保存的代码
    last_updated TIMESTAMP,

    UNIQUE(user_id, question_id),
    INDEX idx_user_status (user_id, status)
);
```

#### 4.2.7 成就表 (achievements)

```sql
CREATE TABLE achievements (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10),  -- emoji
    points INTEGER DEFAULT 0,
    category VARCHAR(50),  -- basic/special/expert
    condition_type VARCHAR(50),  -- question_count/streak/perfect等
    condition_value INTEGER,

    INDEX idx_category (category)
);
```

#### 4.2.8 用户成就关联表 (user_achievements)

```sql
CREATE TABLE user_achievements (
    user_id INTEGER REFERENCES users(id),
    achievement_id VARCHAR(50) REFERENCES achievements(id),
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, achievement_id),
    INDEX idx_user (user_id),
    INDEX idx_earned_at (earned_at)
);
```

#### 4.2.9 知识点表 (knowledge_points)

```sql
CREATE TABLE knowledge_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE,
    category VARCHAR(50),
    description TEXT,
    parent_id INTEGER REFERENCES knowledge_points(id),

    INDEX idx_category (category),
    INDEX idx_parent (parent_id)
);
```

#### 4.2.10 题目-知识点关联表 (question_knowledge)

```sql
CREATE TABLE question_knowledge (
    question_id VARCHAR(20) REFERENCES questions(id),
    knowledge_id INTEGER REFERENCES knowledge_points(id),

    PRIMARY KEY (question_id, knowledge_id),
    INDEX idx_question (question_id),
    INDEX idx_knowledge (knowledge_id)
);
```

#### 4.2.11 学习小组表 (study_groups)

```sql
CREATE TABLE study_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    level INTEGER DEFAULT 1,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_created_by (created_by)
);
```

#### 4.2.12 小组成员表 (group_members)

```sql
CREATE TABLE group_members (
    group_id INTEGER REFERENCES study_groups(id),
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member',  -- owner/admin/member
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (group_id, user_id),
    INDEX idx_group (group_id),
    INDEX idx_user (user_id)
);
```

#### 4.2.13 挑战赛表 (challenges)

```sql
CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'upcoming',  -- upcoming/active/ended
    created_by INTEGER REFERENCES users(id),

    INDEX idx_status (status),
    INDEX idx_time (start_time, end_time)
);
```

#### 4.2.14 每日任务表 (daily_tasks)

```sql
CREATE TABLE daily_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50),  -- login/complete_question/study_time等
    target INTEGER,  -- 目标值
    points INTEGER DEFAULT 10,  -- 奖励积分
    is_active BOOLEAN DEFAULT TRUE
);
```

#### 4.2.15 用户任务完成记录表 (user_task_completions)

```sql
CREATE TABLE user_task_completions (
    user_id INTEGER REFERENCES users(id),
    task_id INTEGER REFERENCES daily_tasks(id),
    completed_at DATE,
    progress INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (user_id, task_id, completed_at),
    INDEX idx_user_date (user_id, completed_at)
);
```

### 4.3 数据库索引策略

**主要索引**:
1. 用户表: username, email（唯一索引）
2. 题目表: category, difficulty, type（组合索引）
3. 提交表: user_id, question_id, submitted_at（组合索引）
4. 进度表: user_id, status（组合索引）

**查询优化**:
- 使用EXPLAIN分析慢查询
- 对高频查询字段建立索引
- 避免SELECT *，只查询需要的字段
- 使用分页查询，避免一次性加载大量数据

---

## 5. 接口设计

### 5.1 API设计原则

1. **RESTful风格**: 使用标准HTTP方法（GET/POST/PUT/DELETE）
2. **统一响应格式**: 所有API返回统一的JSON格式
3. **版本控制**: URL包含版本号（/api/v1/）
4. **认证机制**: 使用JWT Token认证
5. **错误处理**: 统一的错误码和错误信息

### 5.2 响应格式

**成功响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    ...
  }
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "Invalid input",
  "errors": [
    {
      "field": "username",
      "message": "用户名已存在"
    }
  ]
}
```

### 5.3 API端点设计

#### 5.3.1 认证相关API

**POST /api/v1/auth/register** - 用户注册

请求:
```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "password": "password123"
}
```

响应:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 1,
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "level": 1,
      "points": 0
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**POST /api/v1/auth/login** - 用户登录

请求:
```json
{
  "username": "zhangsan",
  "password": "password123"
}
```

响应:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {...},
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### 5.3.2 题目相关API

**GET /api/v1/questions** - 获取题目列表

查询参数:
- `category`: 分类筛选
- `difficulty`: 难度筛选
- `type`: 类型筛选
- `page`: 页码（默认1）
- `per_page`: 每页数量（默认20）

响应:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "questions": [
      {
        "id": "STR001",
        "title": "字符串反转",
        "category": "基础入门",
        "difficulty": 1,
        "estimated_time": 5,
        "completed": false
      }
    ],
    "total": 100,
    "page": 1,
    "pages": 5
  }
}
```

**GET /api/v1/questions/:id** - 获取题目详情

响应:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "STR001",
    "title": "字符串反转",
    "description": "编写一个函数...",
    "template": "def reverse_string(s: str) -> str:\n    pass",
    "test_cases": [
      {
        "input": ["hello"],
        "output": "olleh",
        "is_hidden": false
      }
    ],
    "hints": [
      {
        "level": 1,
        "cost": 5
      }
    ]
  }
}
```

**POST /api/v1/questions** - 创建题目（教师）

请求:
```json
{
  "id": "STR002",
  "title": "字符串拼接",
  "type": "coding",
  "category": "基础入门",
  "difficulty": 1,
  "estimated_time": 5,
  "description": "...",
  "template": "...",
  "solution": "...",
  "test_cases": [...]
}
```

#### 5.3.3 提交相关API

**POST /api/v1/submissions** - 提交代码

请求:
```json
{
  "question_id": "STR001",
  "code": "def reverse_string(s: str) -> str:\n    return s[::-1]"
}
```

响应:
```json
{
  "code": 200,
  "message": "执行成功",
  "data": {
    "submission_id": 123,
    "success": true,
    "score": 100,
    "passed": 3,
    "total": 3,
    "execution_time": 0.15,
    "points_earned": 30,
    "results": [
      {
        "test_case": 1,
        "input": ["hello"],
        "expected": "olleh",
        "actual": "olleh",
        "passed": true
      }
    ]
  }
}
```

**GET /api/v1/submissions/:id** - 获取提交详情

**GET /api/v1/submissions/user/:userId** - 获取用户提交历史

#### 5.3.4 学习相关API

**GET /api/v1/progress** - 获取学习进度

响应:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_questions": 100,
    "completed_questions": 45,
    "completion_rate": 0.45,
    "total_time": 3600,  // 秒
    "stages": [
      {
        "name": "基础入门",
        "total": 20,
        "completed": 20,
        "rate": 1.0
      }
    ],
    "knowledge_points": [
      {
        "name": "字符串操作",
        "mastery": 0.95
      }
    ]
  }
}
```

**GET /api/v1/recommendations** - 获取推荐题目

响应:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "recommendations": [
      {
        "question": {...},
        "reason": "巩固算法基础",
        "priority": 0.9
      }
    ]
  }
}
```

**GET /api/v1/reports/weekly** - 获取周报

**GET /api/v1/achievements** - 获取成就列表

---

## 6. 安全设计

### 6.1 认证和授权

#### 6.1.1 JWT Token认证

**Token生成**:
```python
from flask_jwt_extended import create_access_token
from datetime import timedelta

access_token = create_access_token(
    identity=user.id,
    expires_delta=timedelta(hours=24)
)
```

**Token验证**:
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/v1/protected')
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return {'user_id': user_id}
```

**Token刷新**:
```python
@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return {'access_token': new_token}
```

#### 6.1.2 基于角色的访问控制（RBAC）

**角色定义**:
- **Student**: 学生，基础权限
- **Teacher**: 教师，可创建/编辑题目
- **Admin**: 管理员，所有权限

**权限装饰器**:
```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if user.role != role and user.role != 'admin':
                return jsonify({
                    'code': 403,
                    'message': '权限不足'
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@app.route('/api/v1/questions', methods=['POST'])
@role_required('teacher')
def create_question():
    # 只有教师和管理员可以创建题目
    pass
```

### 6.2 代码执行安全

#### 6.2.1 Docker容器隔离

**容器配置**:
```python
container_config = {
    'image': 'python:3.9-alpine',
    'mem_limit': '128m',           # 内存限制128MB
    'cpu_period': 100000,          # CPU周期
    'cpu_quota': 50000,            # CPU配额（50%）
    'network_disabled': True,      # 禁用网络
    'read_only': True,             # 只读文件系统
    'security_opt': ['no-new-privileges'],  # 禁止提权
    'cap_drop': ['ALL'],           # 移除所有能力
    'pids_limit': 50,              # 进程数限制
    'timeout': 5                   # 超时5秒
}
```

#### 6.2.2 代码静态分析

**AST分析禁止危险操作**:
```python
import ast

FORBIDDEN_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'urllib',
    'requests', 'shutil', 'pickle', 'eval', 'exec'
}

FORBIDDEN_FUNCTIONS = {
    'eval', 'exec', 'compile', '__import__',
    'open', 'input', 'raw_input'
}

class SecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in FORBIDDEN_MODULES:
                self.violations.append(
                    f'禁止导入模块: {alias.name}'
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in FORBIDDEN_MODULES:
            self.violations.append(
                f'禁止导入模块: {node.module}'
            )
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_FUNCTIONS:
                self.violations.append(
                    f'禁止调用函数: {node.func.id}'
                )
        self.generic_visit(node)

def check_code_security(code: str) -> List[str]:
    """检查代码安全性"""
    try:
        tree = ast.parse(code)
        checker = SecurityChecker()
        checker.visit(tree)
        return checker.violations
    except SyntaxError as e:
        return [f'语法错误: {str(e)}']
```

#### 6.2.3 资源限制

**执行时间限制**:
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError('代码执行超时')

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5秒超时

try:
    # 执行代码
    exec(code)
except TimeoutError:
    print('执行超时')
finally:
    signal.alarm(0)  # 取消超时
```

### 6.3 数据安全

#### 6.3.1 密码安全

**密码强度验证**:
```python
import re

def validate_password(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 8 or len(password) > 20:
        return False

    # 必须包含字母和数字
    if not re.search(r'[a-zA-Z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True
```

**密码加密**:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# 加密
password_hash = generate_password_hash(
    password,
    method='pbkdf2:sha256',
    salt_length=16
)

# 验证
is_valid = check_password_hash(password_hash, password)
```

#### 6.3.2 SQL注入防护

**使用ORM参数化查询**:
```python
# ✅ 安全：使用ORM
user = User.query.filter_by(username=username).first()

# ✅ 安全：参数化查询
user = db.session.execute(
    'SELECT * FROM users WHERE username = :username',
    {'username': username}
).first()

# ❌ 危险：字符串拼接
query = f"SELECT * FROM users WHERE username = '{username}'"
```

#### 6.3.3 XSS防护

**输出转义**:
```python
from markupsafe import escape

# 转义HTML
safe_text = escape(user_input)

# Vue.js自动转义
<template>
  <div>{{ userInput }}</div>  <!-- 自动转义 -->
  <div v-html="userInput"></div>  <!-- 不转义，慎用 -->
</template>
```

#### 6.3.4 CSRF防护

**CSRF Token**:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# 前端发送请求时携带CSRF Token
headers = {
    'X-CSRFToken': csrf_token
}
```

### 6.4 文件上传安全

**文件类型和大小限制**:
```python
ALLOWED_EXTENSIONS = {'py', 'txt', 'yaml', 'yml'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': '没有文件'}, 400

    file = request.files['file']

    # 检查文件名
    if not allowed_file(file.filename):
        return {'error': '不支持的文件类型'}, 400

    # 检查文件大小
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        return {'error': '文件过大'}, 400

    # 保存文件
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return {'success': True}
```

---

## 7. 性能设计

### 7.1 缓存策略

#### 7.1.1 应用层缓存

**内存缓存（LRU Cache）**:
```python
from functools import lru_cache
from cachetools import TTLCache

# 题目列表缓存（5分钟）
question_cache = TTLCache(maxsize=100, ttl=300)

@lru_cache(maxsize=128)
def get_question_by_id(question_id):
    """获取题目详情（带缓存）"""
    if question_id in question_cache:
        return question_cache[question_id]

    question = Question.query.get(question_id)
    question_cache[question_id] = question
    return question

# 用户信息缓存（10分钟）
user_cache = TTLCache(maxsize=500, ttl=600)

def get_user_by_id(user_id):
    """获取用户信息（带缓存）"""
    if user_id in user_cache:
        return user_cache[user_id]

    user = User.query.get(user_id)
    user_cache[user_id] = user
    return user
```

**缓存失效策略**:
- 题目更新时清除题目缓存
- 用户信息更新时清除用户缓存
- 排行榜每5分钟更新一次
- 学习进度实时更新，不缓存

#### 7.1.2 数据库查询优化

**索引优化**:
```sql
-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 题目表索引
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_type ON questions(type);

-- 提交表索引
CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_question_id ON submissions(question_id);
CREATE INDEX idx_submissions_submitted_at ON submissions(submitted_at);
CREATE INDEX idx_submissions_user_question ON submissions(user_id, question_id);

-- 进度表索引
CREATE INDEX idx_progress_user_id ON progress(user_id);
CREATE INDEX idx_progress_user_status ON progress(user_id, status);
```

**查询优化**:
```python
# ❌ 避免N+1查询
users = User.query.all()
for user in users:
    submissions = user.submissions  # 每次都查询数据库

# ✅ 使用join预加载
from sqlalchemy.orm import joinedload

users = User.query.options(
    joinedload(User.submissions)
).all()

# ✅ 只查询需要的字段
users = db.session.query(
    User.id,
    User.username,
    User.level
).all()

# ✅ 使用分页
from flask_sqlalchemy import Pagination

page = request.args.get('page', 1, type=int)
per_page = 20

pagination = Question.query.paginate(
    page=page,
    per_page=per_page,
    error_out=False
)
```

### 7.2 异步处理

#### 7.2.1 代码执行异步化

**使用线程池**:
```python
from concurrent.futures import ThreadPoolExecutor
import threading

# 创建线程池
executor = ThreadPoolExecutor(max_workers=10)

def execute_code_async(submission_id, code, test_cases):
    """异步执行代码"""
    def run():
        try:
            result = executor_service.execute(code, test_cases)

            # 更新提交记录
            submission = Submission.query.get(submission_id)
            submission.result = result
            submission.success = result['success']
            submission.score = result['score']
            db.session.commit()

        except Exception as e:
            logger.error(f'代码执行失败: {e}')

    # 提交到线程池
    executor.submit(run)

@app.route('/api/v1/submissions', methods=['POST'])
def submit_code():
    data = request.json

    # 创建提交记录
    submission = Submission(
        user_id=get_jwt_identity(),
        question_id=data['question_id'],
        code=data['code'],
        status='pending'
    )
    db.session.add(submission)
    db.session.commit()

    # 异步执行
    execute_code_async(submission.id, data['code'], test_cases)

    return {
        'submission_id': submission.id,
        'status': 'pending'
    }
```

#### 7.2.2 后台任务

**定时任务**:
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# 每日备份任务
@scheduler.scheduled_job('cron', hour=2, minute=0)
def daily_backup():
    """每日凌晨2点备份数据库"""
    backup_database()

# 每小时清理过期数据
@scheduler.scheduled_job('cron', minute=0)
def hourly_cleanup():
    """每小时清理过期数据"""
    cleanup_expired_data()

# 每5分钟更新排行榜
@scheduler.scheduled_job('interval', minutes=5)
def update_leaderboard():
    """更新排行榜"""
    calculate_leaderboard()

scheduler.start()
```

### 7.3 数据库连接池

**SQLAlchemy连接池配置**:
```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,          # 连接池大小
    'pool_recycle': 3600,     # 连接回收时间（秒）
    'pool_pre_ping': True,    # 连接前检查
    'max_overflow': 20,       # 最大溢出连接数
    'pool_timeout': 30        # 获取连接超时时间
}
```

### 7.4 前端性能优化

#### 7.4.1 代码分割

**Vue Router懒加载**:
```javascript
const routes = [
  {
    path: '/',
    component: () => import('./views/Home.vue')
  },
  {
    path: '/questions',
    component: () => import('./views/QuestionList.vue')
  },
  {
    path: '/questions/:id',
    component: () => import('./views/QuestionDetail.vue')
  }
]
```

#### 7.4.2 资源优化

**Vite构建优化**:
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'editor': ['codemirror'],
          'charts': ['chart.js']
        }
      }
    },
    chunkSizeWarningLimit: 500,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
}
```

#### 7.4.3 图片优化

- 使用WebP格式
- 图片懒加载
- 响应式图片
- CDN加速

### 7.5 API性能优化

#### 7.5.1 响应压缩

```python
from flask_compress import Compress

compress = Compress()
compress.init_app(app)

app.config['COMPRESS_MIMETYPES'] = [
    'text/html',
    'text/css',
    'text/javascript',
    'application/json'
]
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500
```

#### 7.5.2 请求限流

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/submissions', methods=['POST'])
@limiter.limit("10 per minute")
def submit_code():
    """提交代码（限流：每分钟10次）"""
    pass

@app.route('/api/v1/questions')
@limiter.limit("100 per minute")
def get_questions():
    """获取题目列表（限流：每分钟100次）"""
    pass
```

---

## 8. 部署设计

### 8.1 Docker容器化部署

#### 7.1.1 目录结构

```
pythonLearn/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── nginx.conf
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── data/
    ├── pythonlearn.db
    └── questions/
```

#### 7.1.2 Docker Compose配置

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    container_name: pythonlearn-frontend
    ports:
      - "3000:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
    restart: unless-stopped

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: ../Dockerfile.backend
    container_name: pythonlearn-backend
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./backend:/app
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:////app/data/pythonlearn.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    restart: unless-stopped

  # Nginx反向代理
  nginx:
    image: nginx:1.21-alpine
    container_name: pythonlearn-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  data:
```

#### 7.1.3 后端Dockerfile

**Dockerfile.backend**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

#### 7.1.4 前端Dockerfile

**Dockerfile.frontend**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci

# 构建应用
COPY . .
RUN npm run build

# 生产环境
FROM nginx:1.21-alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 7.1.5 Nginx配置

**nginx.conf**:
```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream backend {
        server backend:5000;
    }

    server {
        listen 80;
        server_name localhost;

        # 前端静态文件
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # API代理
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket支持
        location /ws/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### 7.2 部署流程

#### 7.2.1 一键部署脚本

**deploy.sh**:
```bash
#!/bin/bash

echo "🚀 开始部署pythonLearn..."

# 1. 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 2. 检查Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 3. 生成JWT密钥
if [ ! -f .env ]; then
    echo "📝 生成配置文件..."
    echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" > .env
fi

# 4. 创建数据目录
mkdir -p data/questions

# 5. 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 6. 启动服务
echo "▶️  启动服务..."
docker-compose up -d

# 7. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 8. 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo "✅ 部署成功！"
    echo "📖 访问地址: http://localhost"
    echo "📊 后端API: http://localhost/api/v1"
else
    echo "❌ 部署失败，请检查日志"
    docker-compose logs
    exit 1
fi
```

#### 7.2.2 数据库初始化

**init_db.py**:
```python
from app import create_app, db
from app.models import User, Question, Achievement

app = create_app()

with app.app_context():
    # 创建表
    db.create_all()

    # 创建管理员账户
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)

    # 初始化成就
    achievements = [
        Achievement(
            id='first_question',
            name='新手上路',
            description='完成第1道题',
            icon='🎓',
            points=10
        ),
        # ... 更多成就
    ]
    db.session.bulk_save_objects(achievements)

    db.session.commit()
    print('✅ 数据库初始化完成')
```

### 7.3 运维管理

#### 7.3.1 日志管理

**日志配置**:
```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=10
)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
```

**查看日志**:
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend

# 实时查看日志
docker-compose logs -f backend
```

#### 7.3.2 数据备份

**备份脚本 (backup.sh)**:
```bash
#!/bin/bash

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
echo "📦 备份数据库..."
cp data/pythonlearn.db $BACKUP_DIR/pythonlearn_$DATE.db

# 备份题目文件
echo "📦 备份题目文件..."
tar -czf $BACKUP_DIR/questions_$DATE.tar.gz data/questions/

# 删除30天前的备份
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "✅ 备份完成: $BACKUP_DIR"
```

#### 7.3.3 监控和健康检查

**健康检查端点**:
```python
@app.route('/api/v1/health')
def health_check():
    try:
        # 检查数据库连接
        db.session.execute('SELECT 1')

        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 500
```

---

## 9. 运维设计

### 9.1 监控系统

#### 9.1.1 系统监控

**监控指标**:
```python
from prometheus_client import Counter, Histogram, Gauge
import psutil

# 请求计数器
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# 响应时间直方图
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# 系统资源监控
cpu_usage = Gauge('system_cpu_usage', 'CPU usage percentage')
memory_usage = Gauge('system_memory_usage', 'Memory usage percentage')
disk_usage = Gauge('system_disk_usage', 'Disk usage percentage')

def update_system_metrics():
    """更新系统指标"""
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    disk_usage.set(psutil.disk_usage('/').percent)

# 定时更新
scheduler.add_job(update_system_metrics, 'interval', seconds=30)
```

**监控端点**:
```python
from prometheus_client import generate_latest

@app.route('/metrics')
def metrics():
    """Prometheus监控端点"""
    return generate_latest()
```

#### 9.1.2 业务监控

**关键业务指标**:
```python
# 用户指标
user_register_count = Counter('user_register_total', 'Total user registrations')
user_login_count = Counter('user_login_total', 'Total user logins')
active_users = Gauge('active_users', 'Current active users')

# 学习指标
question_submit_count = Counter('question_submit_total', 'Total question submissions')
question_pass_count = Counter('question_pass_total', 'Total question passes')
question_pass_rate = Gauge('question_pass_rate', 'Question pass rate')

# 代码执行指标
code_execution_count = Counter('code_execution_total', 'Total code executions')
code_execution_duration = Histogram(
    'code_execution_duration_seconds',
    'Code execution duration'
)
code_execution_errors = Counter('code_execution_errors_total', 'Total code execution errors')
```

### 9.2 告警系统

#### 9.2.1 告警规则

**告警配置**:
```yaml
# alerts.yml
groups:
  - name: system_alerts
    rules:
      # CPU使用率告警
      - alert: HighCPUUsage
        expr: system_cpu_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU使用率过高"
          description: "CPU使用率超过80%，当前值: {{ $value }}%"

      # 内存使用率告警
      - alert: HighMemoryUsage
        expr: system_memory_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "内存使用率过高"
          description: "内存使用率超过80%，当前值: {{ $value }}%"

      # 磁盘空间告警
      - alert: LowDiskSpace
        expr: system_disk_usage > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "磁盘空间不足"
          description: "磁盘使用率超过90%，当前值: {{ $value }}%"

      # API响应时间告警
      - alert: SlowAPIResponse
        expr: http_request_duration_seconds > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API响应时间过长"
          description: "API响应时间超过2秒"

      # 错误率告警
      - alert: HighErrorRate
        expr: rate(code_execution_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "代码执行错误率过高"
          description: "代码执行错误率超过5%"
```

#### 9.2.2 告警通知

**邮件通知**:
```python
import smtplib
from email.mime.text import MIMEText

def send_alert_email(subject, content, recipients):
    """发送告警邮件"""
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = 'alert@pythonlearn.com'
    msg['To'] = ', '.join(recipients)

    try:
        smtp = smtplib.SMTP('smtp.example.com', 587)
        smtp.starttls()
        smtp.login('alert@pythonlearn.com', 'password')
        smtp.send_message(msg)
        smtp.quit()
        logger.info(f'告警邮件已发送: {subject}')
    except Exception as e:
        logger.error(f'发送告警邮件失败: {e}')
```

### 9.3 日志管理

#### 9.3.1 日志分类

**日志级别和用途**:
```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 访问日志
access_logger = logging.getLogger('access')
access_handler = TimedRotatingFileHandler(
    'logs/access.log',
    when='midnight',
    interval=1,
    backupCount=30
)
access_logger.addHandler(access_handler)

# 错误日志
error_logger = logging.getLogger('error')
error_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=10*1024*1024,
    backupCount=10
)
error_logger.addHandler(error_handler)

# 业务日志
business_logger = logging.getLogger('business')
business_handler = RotatingFileHandler(
    'logs/business.log',
    maxBytes=10*1024*1024,
    backupCount=10
)
business_logger.addHandler(business_handler)

# 安全日志
security_logger = logging.getLogger('security')
security_handler = RotatingFileHandler(
    'logs/security.log',
    maxBytes=10*1024*1024,
    backupCount=30
)
security_logger.addHandler(security_handler)
```

#### 9.3.2 结构化日志

```python
import json
from datetime import datetime

def log_structured(logger, level, event, **kwargs):
    """记录结构化日志"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'event': event,
        **kwargs
    }

    logger.log(
        getattr(logging, level),
        json.dumps(log_entry, ensure_ascii=False)
    )

# 使用示例
log_structured(
    business_logger,
    'INFO',
    'user_login',
    user_id=123,
    username='zhangsan',
    ip='192.168.1.100'
)

log_structured(
    security_logger,
    'WARNING',
    'login_failed',
    username='admin',
    ip='192.168.1.200',
    reason='invalid_password'
)
```

### 9.4 故障处理

#### 9.4.1 故障分类

| 故障级别 | 响应时间 | 处理流程 |
|---------|---------|---------|
| P0 - 紧急 | 15分钟 | 立即处理，通知所有相关人员 |
| P1 - 高 | 1小时 | 优先处理，通知负责人 |
| P2 - 中 | 4小时 | 正常处理，记录问题 |
| P3 - 低 | 1天 | 计划处理，定期回顾 |

#### 9.4.2 故障处理流程

**故障响应流程**:
```
1. 故障发现
   ↓
2. 故障确认
   ↓
3. 影响评估
   ↓
4. 应急处理
   ↓
5. 根因分析
   ↓
6. 永久修复
   ↓
7. 复盘总结
```

**故障处理脚本**:
```bash
#!/bin/bash
# emergency_restart.sh - 紧急重启脚本

echo "🚨 开始紧急重启..."

# 1. 备份当前状态
echo "📦 备份当前数据..."
./backup.sh

# 2. 停止服务
echo "⏸️  停止服务..."
docker-compose down

# 3. 清理临时文件
echo "🧹 清理临时文件..."
rm -rf /tmp/pythonlearn/*

# 4. 启动服务
echo "▶️  启动服务..."
docker-compose up -d

# 5. 健康检查
echo "🔍 健康检查..."
sleep 10
curl -f http://localhost/api/v1/health || exit 1

echo "✅ 重启完成"
```

### 9.5 容量规划

#### 9.5.1 资源需求预测

**当前资源使用**（500用户）:
- CPU: 2核，平均使用率30%
- 内存: 4GB，平均使用率50%
- 磁盘: 20GB，使用10GB
- 网络: 10Mbps，平均流量2Mbps

**1年后预测**（1000用户）:
- CPU: 4核
- 内存: 8GB
- 磁盘: 50GB
- 网络: 20Mbps

#### 9.5.2 扩容策略

**垂直扩容**（单机性能不足时）:
1. 增加CPU核心数
2. 增加内存容量
3. 升级磁盘（SSD）
4. 增加网络带宽

**水平扩容**（需要高可用时）:
1. 部署多个后端实例
2. 使用Nginx负载均衡
3. 数据库读写分离
4. 使用Redis缓存

### 9.6 灾难恢复

#### 9.6.1 备份策略

**备份类型**:
- **全量备份**: 每周日凌晨2点
- **增量备份**: 每天凌晨2点
- **实时备份**: 关键操作实时备份

**备份内容**:
- 数据库文件
- 题目文件
- 配置文件
- 日志文件

**备份验证**:
```bash
#!/bin/bash
# verify_backup.sh - 验证备份文件

BACKUP_FILE=$1

echo "🔍 验证备份文件: $BACKUP_FILE"

# 1. 检查文件存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 备份文件不存在"
    exit 1
fi

# 2. 检查文件大小
SIZE=$(stat -f%z "$BACKUP_FILE")
if [ $SIZE -lt 1000000 ]; then
    echo "❌ 备份文件过小"
    exit 1
fi

# 3. 尝试解压
tar -tzf "$BACKUP_FILE" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 备份文件损坏"
    exit 1
fi

echo "✅ 备份文件验证通过"
```

#### 9.6.2 恢复流程

**数据恢复步骤**:
```bash
#!/bin/bash
# restore.sh - 数据恢复脚本

BACKUP_FILE=$1

echo "🔄 开始数据恢复..."

# 1. 停止服务
echo "⏸️  停止服务..."
docker-compose down

# 2. 备份当前数据
echo "📦 备份当前数据..."
mv data data.old.$(date +%Y%m%d_%H%M%S)

# 3. 解压备份文件
echo "📂 解压备份文件..."
tar -xzf "$BACKUP_FILE" -C .

# 4. 启动服务
echo "▶️  启动服务..."
docker-compose up -d

# 5. 验证数据
echo "🔍 验证数据..."
sleep 10
python verify_data.py

echo "✅ 数据恢复完成"
```

---

## 附录

### A. 技术选型对比

详见 [技术栈对比文档](TECH_STACK_COMPARISON.md)

### B. 性能测试报告

**测试环境**:
- CPU: 4核
- 内存: 8GB
- 数据库: SQLite
- 并发用户: 100

**测试结果**:
| 指标 | 结果 |
|------|------|
| 页面加载时间 | 0.8秒 |
| API响应时间 | 120ms |
| 代码执行时间 | 2.5秒 |
| 并发QPS | 350 |
| 数据库查询 | 35ms |

### C. 开发规范

**代码规范**:
- Python: PEP 8
- JavaScript: ESLint + Prettier
- Git提交: Conventional Commits

**分支策略**:
- `main`: 生产环境
- `develop`: 开发环境
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复

---

**文档结束**

**编写**: 开发团队
**审核**: 待定
**批准**: 待定
**日期**: 2025-11-07


