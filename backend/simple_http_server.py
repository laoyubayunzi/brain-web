# 使用Python内置模块创建简单HTTP服务器，不依赖任何第三方库
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

def create_simple_server():
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # 设置所有请求的CORS头
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            
            # 处理不同的路径
            if self.path == '/api/test' or self.path == '/api/apply' or self.path == '/api/contact' or self.path == '/api/newsletter' or self.path == '/api/stats':
                # 发送200响应和JSON内容
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # 根据不同的端点返回不同的响应
                endpoint = self.path.replace('/api/', '')
                
                if endpoint == 'test':
                    response_data = {
                        'success': True,
                        'message': 'API服务运行正常！',
                        'timestamp': time.time()
                    }
                elif endpoint == 'stats':
                    # 返回统计数据，用于图表显示
                    response_data = {
                        'success': True,
                        'members': 120,
                        'projects': 25,
                        'events': 18,
                        'departments': [
                            { 'name': '脑机接口', 'value': 35 },
                            { 'name': '人工智能', 'value': 25 },
                            { 'name': '计算机视觉', 'value': 20 },
                            { 'name': '自然语言处理', 'value': 15 },
                            { 'name': '其他', 'value': 5 }
                        ]
                    }
                else:
                    # 对于其他API端点（apply、contact、newsletter）
                    response_data = {
                        'success': True,
                        'message': f'成功提交到 {endpoint} 端点！',
                        'timestamp': time.time()
                    }
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                print(f"[INFO] 处理请求: {self.path}, IP: {self.client_address[0]}")
                
            elif self.path == '/' or self.path == '/api':
                # 发送200响应和JSON内容
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'status': 'running',
                    'message': 'SAU脑机与人工智能俱乐部后端服务',
                    'version': '1.0.0',
                    'available_endpoints': [
                        '/api/test',
                        '/api/apply',
                        '/api/contact',
                        '/api/newsletter',
                        '/api/stats'
                    ],
                    'timestamp': time.time()
                }
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                print(f"[INFO] 处理请求: {self.path}, IP: {self.client_address[0]}")
                
            else:
                # 处理404
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'error': 'Not Found',
                    'path': self.path,
                    'available_endpoints': [
                        '/api/test',
                        '/api/apply',
                        '/api/contact',
                        '/api/newsletter',
                        '/api/stats'
                    ]
                }
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                print(f"[WARNING] 404未找到: {self.path}, IP: {self.client_address[0]}")
        
        def do_OPTIONS(self):
            # 处理预检请求
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.end_headers()
            print(f"[INFO] 处理预检请求: {self.path}, IP: {self.client_address[0]}")
            
        def do_POST(self):
            # 设置所有请求的CORS头
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            
            # 处理POST请求
            if self.path.startswith('/api/'):
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                # 尝试解析JSON
                try:
                    data = json.loads(post_data)
                except json.JSONDecodeError:
                    data = {}
                
                # 发送成功响应
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                endpoint = self.path.replace('/api/', '')
                response_data = {
                    'success': True,
                    'message': f'成功接收到 {endpoint} 的POST数据！',
                    'received_data': data,
                    'timestamp': time.time()
                }
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                print(f"[INFO] 处理POST请求: {self.path}, IP: {self.client_address[0]}")
                print(f"[INFO] 接收到的数据: {post_data}")
                
            else:
                # 其他POST请求返回404
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'error': 'Not Found',
                    'path': self.path
                }
                
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                print(f"[WARNING] 404未找到(POST): {self.path}, IP: {self.client_address[0]}")
        
        def log_message(self, format, *args):
            # 禁用默认日志，使用自定义日志
            pass
    
    # 启动服务器，使用端口8000并绑定到所有地址
    port = 8000
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"[INFO] 简单HTTP服务器启动在 http://127.0.0.1:{port}")
    print(f"[INFO] 测试端点: http://127.0.0.1:{port}/api/test")
    print(f"[INFO] 根路径: http://127.0.0.1:{port}/")
    print(f"[INFO] 按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] 正在关闭服务器...")
        httpd.server_close()
        print("[INFO] 服务器已关闭")

if __name__ == '__main__':
    create_simple_server()
