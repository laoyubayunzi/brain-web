#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAU脑机与人工智能俱乐部网站 - 部署测试脚本
此脚本用于验证部署后的网站功能是否正常工作
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# 默认配置
DEFAULT_API_BASE = "http://localhost:8000/api"
DEFAULT_FRONTEND_URL = "http://localhost"
TIMEOUT = 10  # 超时时间（秒）

# 测试结果统计
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

def print_header():
    """打印测试脚本标题"""
    print("=" * 60)
    print("SAU脑机与人工智能俱乐部网站 - 部署测试")
    print("=" * 60)
    print()

def print_section(title):
    """打印测试区块标题"""
    print(f"\n{'-' * 60}")
    print(f"{title}")
    print(f"{'-' * 60}")

def print_result(test_name, success, message=None):
    """打印单个测试结果"""
    results["total"] += 1
    status = "✓ 通过" if success else "✗ 失败"
    print(f"[{status}] {test_name}")
    
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
        error_msg = message if message else "未知错误"
        results["errors"].append(f"{test_name}: {error_msg}")

def test_api_endpoints(api_base_url):
    """测试后端API端点"""
    print_section("测试后端API端点")
    
    # 要测试的API端点列表
    endpoints = [
        ("GET", "/stats", "获取统计数据"),
        ("GET", "/events", "获取活动列表"),
    ]
    
    for method, endpoint, description in endpoints:
        full_url = urljoin(api_base_url, endpoint.lstrip('/'))
        test_name = f"{method} {endpoint} - {description}"
        
        try:
            if method == "GET":
                response = requests.get(full_url, timeout=TIMEOUT)
                response.raise_for_status()
                
                # 检查响应格式是否为JSON
                data = response.json()
                print_result(test_name, True, f"响应状态码: {response.status_code}")
            
        except requests.exceptions.Timeout:
            print_result(test_name, False, "请求超时")
        except requests.exceptions.ConnectionError:
            print_result(test_name, False, "连接错误，请检查服务是否运行")
        except requests.exceptions.HTTPError as e:
            print_result(test_name, False, f"HTTP错误: {str(e)}")
        except json.JSONDecodeError:
            print_result(test_name, False, "响应不是有效的JSON格式")
        except Exception as e:
            print_result(test_name, False, f"发生异常: {str(e)}")
    
    # 测试一些POST端点（模拟表单提交）
    test_post_endpoints(api_base_url)

def test_post_endpoints(api_base_url):
    """测试POST API端点"""
    print_section("测试POST API端点（模拟表单提交）")
    
    # 模拟订阅通讯测试
    subscribe_url = urljoin(api_base_url, "newsletter")
    test_name = "POST /newsletter - 模拟订阅通讯"
    
    try:
        test_email = f"test_{int(time.time())}@example.com"  # 使用时间戳生成唯一邮箱
        payload = {"email": test_email}
        response = requests.post(subscribe_url, json=payload, timeout=TIMEOUT)
        
        # 在测试环境中，即使返回400（已存在）也视为通过，因为API在正常响应
        if response.status_code in [200, 201, 400]:
            print_result(test_name, True, f"响应状态码: {response.status_code}")
        else:
            print_result(test_name, False, f"意外的状态码: {response.status_code}")
    
    except Exception as e:
        print_result(test_name, False, f"发生异常: {str(e)}")

def test_frontend_connection(frontend_url):
    """测试前端页面连接"""
    print_section("测试前端页面连接")
    
    test_pages = [
        ("", "首页"),
        ("privacy.html", "隐私政策页面"),
        ("terms.html", "使用条款页面"),
        ("cookie.html", "Cookie政策页面"),
    ]
    
    for path, description in test_pages:
        full_url = urljoin(frontend_url, path)
        test_name = f"GET {path} - {description}"
        
        try:
            response = requests.get(full_url, timeout=TIMEOUT)
            response.raise_for_status()
            print_result(test_name, True, f"响应状态码: {response.status_code}")
        except requests.exceptions.Timeout:
            print_result(test_name, False, "请求超时")
        except requests.exceptions.ConnectionError:
            print_result(test_name, False, "连接错误，请检查前端服务是否运行")
        except requests.exceptions.HTTPError as e:
            print_result(test_name, False, f"HTTP错误: {str(e)}")
        except Exception as e:
            print_result(test_name, False, f"发生异常: {str(e)}")

def test_api_cors(api_base_url):
    """测试API的CORS配置"""
    print_section("测试API CORS配置")
    test_name = "测试CORS头信息"
    
    try:
        full_url = urljoin(api_base_url, "stats")
        response = requests.get(full_url, timeout=TIMEOUT)
        
        # 检查是否包含CORS相关头
        if 'Access-Control-Allow-Origin' in response.headers:
            print_result(test_name, True, f"CORS已启用: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print_result(test_name, False, "未找到CORS相关头信息")
    
    except Exception as e:
        print_result(test_name, False, f"发生异常: {str(e)}")

def print_summary():
    """打印测试结果摘要"""
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    print(f"总测试数: {results['total']}")
    print(f"通过测试: {results['passed']}")
    print(f"失败测试: {results['failed']}")
    print()
    
    if results['errors']:
        print("失败详情:")
        for i, error in enumerate(results['errors'], 1):
            print(f"{i}. {error}")
        print()
    
    # 打印建议
    if results['failed'] == 0:
        print("🎉 所有测试通过！网站部署成功！")
    elif results['failed'] <= 2:
        print("⚠️  大部分测试通过，但有少量失败。请查看上面的错误详情进行修复。")
    else:
        print("❌ 多个测试失败。请检查以下可能的问题：")
        print("   1. 后端服务是否正常运行？")
        print("   2. 数据库连接是否正确？")
        print("   3. 防火墙设置是否允许相应端口？")
        print("   4. Nginx配置是否正确？")

def main():
    """主函数"""
    print_header()
    
    # 获取命令行参数（如果提供）
    api_base_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_API_BASE
    frontend_url = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_FRONTEND_URL
    
    print(f"测试配置：")
    print(f"- API基础URL: {api_base_url}")
    print(f"- 前端URL: {frontend_url}")
    print(f"- 超时时间: {TIMEOUT}秒")
    print()
    
    # 执行测试
    test_api_endpoints(api_base_url)
    test_api_cors(api_base_url)
    test_frontend_connection(frontend_url)
    
    # 打印摘要
    print_summary()
    
    # 返回状态码
    sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()
