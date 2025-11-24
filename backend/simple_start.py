from flask import Flask, jsonify
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 简单的CORS处理
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/test', methods=['GET'])
def test_api():
    logger.info("接收到API测试请求")
    return jsonify({'success': True, 'message': 'API服务运行正常！'})

@app.route('/', methods=['GET'])
def index():
    logger.info("接收到根路径请求")
    return jsonify({'status': 'running', 'message': 'SAU脑机与人工智能俱乐部后端服务'})

if __name__ == '__main__':
    # 使用固定端口避免环境变量问题
    port = 5000
    logger.info(f"简单API服务启动在 http://localhost:{port}")
    logger.info(f"测试端点: http://localhost:{port}/api/test")
    # 不使用debug模式避免可能的问题
    app.run(host='127.0.0.1', port=port, debug=False)