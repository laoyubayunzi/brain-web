# SAU脑机与人工智能俱乐部网站 - 后端Dockerfile

# 使用官方Python运行时作为基础镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv venv

# 安装pip依赖
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 复制项目代码
COPY . .

# 创建必要的目录
RUN mkdir -p instance

# 设置正确的权限
RUN chmod -R 755 instance

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "production_start:app"]
