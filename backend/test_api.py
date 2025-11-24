import requests
import time

# 尝试测试API端点
print("正在测试API服务...")
try:
    # 给服务一点时间确保完全启动
    time.sleep(2)
    
    # 测试API端点
    response = requests.get('http://localhost:5000/api/test')
    response.raise_for_status()  # 检查是否有HTTP错误
    
    # 打印响应内容
    print(f"✅ API调用成功！")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 测试根路径
    root_response = requests.get('http://localhost:5000/')
    print(f"\n根路径测试:")
    print(f"状态码: {root_response.status_code}")
    print(f"响应内容: {root_response.json()}")
    
    print("\n🎉 API服务正常运行！'Failed to fetch'错误应该已解决。")
    print("前端现在应该能够正常连接到后端API了。")
    
except requests.exceptions.ConnectionError:
    print("❌ 无法连接到API服务。请确认服务正在运行。")
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
