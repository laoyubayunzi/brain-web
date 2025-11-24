#!/bin/bash

# 激活虚拟环境
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 检查依赖是否已安装
if ! python -c "import flask; import flask_cors; import sqlalchemy; import dotenv; import pandas" 2>/dev/null; then
    echo "安装依赖..."
    pip install -r requirements.txt
fi

# 创建必要的目录
mkdir -p instance

# 启动Gunicorn服务器
echo "启动Gunicorn服务器..."
gunicorn --workers 3 --bind 0.0.0.0:8000 production_start:app --access-logfile - --error-logfile -
