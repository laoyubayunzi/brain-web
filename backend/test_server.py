# 简单的测试脚本，使用Python内置模块测试HTTP服务器
import urllib.request
import json
import time

def test_server():
    print("开始测试HTTP服务器...")
    
    # 测试的URL
    urls = [
        ('API测试端点', 'http://127.0.0.1:5000/api/test'),
        ('根路径', 'http://127.0.0.1:5000/')
    ]
    
    # 添加用户代理和其他头信息
    headers = {
        'User-Agent': 'Python-urllib/3.11',
        'Content-Type': 'application/json'
    }
    
    # 测试每个URL
    all_success = True
    
    for name, url in urls:
        print(f"\n测试 {name}: {url}")
        try:
            # 创建请求
            req = urllib.request.Request(url, headers=headers)
            
            # 发送请求并获取响应
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=5) as response:
                end_time = time.time()
                
                # 读取响应内容
                data = response.read().decode('utf-8')
                status_code = response.status
                
                # 打印响应信息
                print(f"✅ 成功！状态码: {status_code}")
                print(f"响应时间: {((end_time - start_time) * 1000):.2f} ms")
                
                # 尝试解析JSON
                try:
                    json_data = json.loads(data)
                    print(f"响应内容(JSON):")
                    for key, value in json_data.items():
                        print(f"  {key}: {value}")
                except json.JSONDecodeError:
                    print(f"响应内容(非JSON): {data}")
                    
        except Exception as e:
            print(f"❌ 失败！错误: {str(e)}")
            all_success = False
    
    print("\n" + "=" * 50)
    if all_success:
        print("✅ 所有测试都成功了！")
        print("\n后端服务已成功启动并响应请求。")
        print("如果浏览器仍然显示'Failed to fetch'，请检查：")
        print("1. 前端代码中的API URL是否正确设置为http://localhost:5000/api")
        print("2. 浏览器控制台是否有其他错误信息")
        print("3. 尝试刷新浏览器或清除缓存")
    else:
        print("❌ 测试失败，请检查服务器状态。")
    print("=" * 50)

if __name__ == '__main__':
    test_server()
