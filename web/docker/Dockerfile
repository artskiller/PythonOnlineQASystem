# Python学习平台 - Docker镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY web/requirements.txt /app/web/requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r /app/web/requirements.txt

# 复制项目文件
COPY . .

# 设置工作目录为web应用
WORKDIR /app/web

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV PORT=8080
ENV FLASK_ENV=production

# 启动命令
CMD ["python", "app.py"]

