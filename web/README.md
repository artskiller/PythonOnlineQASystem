# 🌐 Web 学习平台

基于Flask的交互式Python学习平台，提供在线代码编辑、实时执行和即时反馈。

<div align="center">
  <img src="../docs/images/web-platform-screenshot.png" alt="Web学习平台界面" width="100%">
  <p><i>现代化的在线编程环境 - 支持实时代码编辑、测试和反馈</i></p>
</div>

---

## 🚀 快速开始

### 方式1：本地运行（推荐）

```bash
# 从项目根目录运行
cd pythonLearn

# 安装依赖
pip install -r web/requirements.txt

# 启动服务
cd web && python app.py

# 浏览器访问
# http://localhost:8080
```

### 方式2：使用Makefile

```bash
# 从项目根目录运行
make web

# 访问 http://localhost:8080
```

### 方式3：Docker部署

```bash
# 从项目根目录运行
cd web/docker
docker-compose up -d

# 访问 http://localhost:8080
```

---

## 📁 目录结构

```
web/
├── README.md              # 本文档
├── app.py                 # Flask应用主文件
├── requirements.txt       # Web应用依赖
├── templates/             # HTML模板
│   └── index.html        # 主页面
├── static/                # 静态资源
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── app.js        # 前端逻辑
└── docker/                # Docker配置
    ├── Dockerfile        # 镜像配置
    └── docker-compose.yml # 编排配置
```

---

## ✨ 核心功能

### 1. 在线代码编辑器
- **CodeMirror** - 专业代码编辑器
- **语法高亮** - Python语法着色
- **自动缩进** - 符合PEP 8规范
- **行号显示** - 方便定位代码

### 2. 实时代码执行
- **即时运行** - 点击按钮立即执行
- **安全沙箱** - 隔离执行环境
- **超时保护** - 30秒自动终止
- **完整输出** - 显示stdout和stderr

### 3. 智能学习辅助
- **💡 查看提示** - 获取解题思路
- **📖 查看答案** - 查看完整答案
- **🔄 重置代码** - 恢复初始状态
- **▶️ 运行测试** - 自动运行测试用例

### 4. 题目管理
- **分类筛选** - 按AI/基础/数据等分类
- **难度筛选** - 按⭐/⭐⭐/⭐⭐⭐筛选
- **实时搜索** - 快速找到目标题目

---

## 🔧 API端点

### GET /
主页面

### GET /api/questions
获取题目列表

**响应**：
```json
[
  {
    "id": "ML1",
    "name": "机器学习基础",
    "category": "AI专项",
    "difficulty": "⭐⭐⭐",
    "time": "90分钟"
  }
]
```

### GET /api/question/<id>
获取题目详情

**响应**：
```json
{
  "id": "ML1",
  "name": "机器学习基础",
  "code": "def encode_categorical_onehot(...):\n    ...",
  "functions": ["encode_categorical_onehot", "..."]
}
```

### POST /api/run
执行代码

**请求**：
```json
{
  "code": "print('Hello, World!')"
}
```

**响应**：
```json
{
  "success": true,
  "output": "Hello, World!\n",
  "error": ""
}
```

---

## 🛠️ 技术栈

### 后端
- **Flask 2.3.0** - Web框架
- **Flask-CORS** - 跨域支持
- **Python 3.8+** - 运行环境

### 前端
- **HTML5** - 语义化标签
- **CSS3** - 现代化样式
- **JavaScript ES6+** - 异步编程
- **CodeMirror 5.65** - 代码编辑器

---

## 🔒 安全特性

1. **代码隔离** - 在临时文件中执行
2. **超时保护** - 30秒自动终止
3. **只读题目** - 题目文件只读挂载
4. **工作目录隔离** - 独立的工作目录

⚠️ **注意**：当前版本适合开发和学习使用，生产环境建议使用Docker容器提供额外隔离。

---

## 📝 配置说明

### 环境变量

- `PORT` - 服务端口（默认：8080）
- `FLASK_ENV` - 运行环境（development/production）

### 自定义端口

```bash
# 使用环境变量
PORT=3000 python app.py

# 访问 http://localhost:3000
```

---

## 🐛 故障排除

### 问题1：无法启动服务

```bash
# 检查依赖
pip list | grep -i flask

# 重新安装
pip install -r requirements.txt
```

### 问题2：端口被占用

```bash
# 使用其他端口
PORT=3000 python app.py
```

### 问题3：静态文件404

确保从 `web/` 目录启动：
```bash
cd web
python app.py
```

或使用Makefile：
```bash
make web
```

---

## 📚 相关文档

- **[Web应用指南](../docs/web-platform/WEB_APP_GUIDE.md)** - 完整使用说明
- **[演示文档](../docs/web-platform/WEB_APP_DEMO.md)** - 快速体验指南
- **[平台总结](../docs/web-platform/WEB_PLATFORM_SUMMARY.md)** - 技术细节

---

## 🚀 开发指南

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（自动重载）
python app.py
```

### 生产部署

```bash
# 使用gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app

# 或使用Docker
cd docker
docker-compose up -d
```

---

**返回 [项目主页](../README.md)**

