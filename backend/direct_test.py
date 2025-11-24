# 直接测试Flask应用，不依赖网络连接
from flask import Flask, jsonify
import sys

def test_flask_app():
    print("开始直接测试Flask应用...")
    
    # 创建一个简单的Flask应用进行测试
    app = Flask(__name__)
    
    @app.route('/api/test')
    def test_route():
        return jsonify({'success': True, 'message': '直接测试成功！'})
    
    # 使用Flask的测试客户端进行测试
    with app.test_client() as client:
        # 发送GET请求到/api/test端点
        response = client.get('/api/test')
        
        # 检查响应
        if response.status_code == 200:
            data = response.get_json()
            print(f"✅ 直接测试成功！")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {data}")
            print("\n这表明Flask框架正常工作。")
            print("如果浏览器仍然显示'Failed to fetch'，可能是以下原因：")
            print("1. 浏览器的跨域问题")
            print("2. 端口冲突")
            print("3. 防火墙阻止")
            print("\n建议解决方案：")
            print("1. 确保前端api.js中的URL设置为http://localhost:5000/api")
            print("2. 尝试使用不同的浏览器")
            print("3. 检查端口5000是否被其他程序占用")
            return True
        else:
            print(f"❌ 直接测试失败，状态码: {response.status_code}")
            return False

if __name__ == '__main__':
    success = test_flask_app()
    sys.exit(0 if success else 1)
