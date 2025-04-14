#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试脚本：测试飞灵(Fatelling)服务器的基本命盘解读API
"""

import requests
import json
import time
import sys

# 服务器地址，可以根据实际情况修改
SERVER_URL = "http://127.0.0.1:8000"  # 默认使用本地服务器地址
API_ENDPOINT = "/api/basic_report"

def test_basic_report():
    """测试基本命盘解读API"""
    print("=== 开始测试基本命盘解读API ===")
    
    # 构建请求数据
    test_data = {
        "gender": "male",
        "year": 1990,
        "month": 10,
        "day": 15,
        "hour": 12,
        "minute": 30
    }
    
    print(f"测试数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送POST请求
        start_time = time.time()
        response = requests.post(
            f"{SERVER_URL}{API_ENDPOINT}", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        # 输出响应状态
        print(f"响应状态码: {response.status_code}")
        print(f"请求处理时间: {end_time - start_time:.2f}秒")
        
        # 如果响应成功，输出结果
        if response.status_code == 200:
            result = response.json()
            print("\n=== 响应结果 ===")
            print(f"八字: {result.get('bazi', '未返回')}")
            print("\n命盘解读:")
            print(result.get('reading', '未返回'))
            print("\n=== 测试成功 ===")
            return True
        else:
            print(f"错误: {response.text}")
            print("\n=== 测试失败 ===")
            return False
    
    except Exception as e:
        print(f"发生异常: {str(e)}")
        print("\n=== 测试失败 ===")
        return False

def test_with_female_data():
    """使用女性数据测试API"""
    print("\n=== 开始使用女性数据测试 ===")
    
    # 女性测试数据
    test_data = {
        "gender": "female",
        "year": 1992,
        "month": 5,
        "day": 20,
        "hour": 8,
        "minute": 15
    }
    
    print(f"测试数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送POST请求
        start_time = time.time()
        response = requests.post(
            f"{SERVER_URL}{API_ENDPOINT}", 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        # 输出响应状态
        print(f"响应状态码: {response.status_code}")
        print(f"请求处理时间: {end_time - start_time:.2f}秒")
        
        # 如果响应成功，输出结果
        if response.status_code == 200:
            result = response.json()
            print("\n=== 响应结果 ===")
            print(f"八字: {result.get('bazi', '未返回')}")
            print("\n命盘解读:")
            print(result.get('reading', '未返回'))
            print("\n=== 测试成功 ===")
            return True
        else:
            print(f"错误: {response.text}")
            print("\n=== 测试失败 ===")
            return False
    
    except Exception as e:
        print(f"发生异常: {str(e)}")
        print("\n=== 测试失败 ===")
        return False

def test_invalid_data():
    """测试无效数据的处理"""
    print("\n=== 开始测试无效数据处理 ===")
    
    # 无效数据（年份超出范围）
    invalid_data = {
        "gender": "male",
        "year": 2200,  # 超出有效范围
        "month": 10,
        "day": 15,
        "hour": 12,
        "minute": 30
    }
    
    print(f"无效测试数据: {json.dumps(invalid_data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送POST请求
        response = requests.post(
            f"{SERVER_URL}{API_ENDPOINT}", 
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 输出响应状态
        print(f"响应状态码: {response.status_code}")
        
        # 预期应该返回错误
        if response.status_code != 200:
            print(f"错误信息: {response.text}")
            print("=== 测试通过：成功捕获无效数据 ===")
            return True
        else:
            print("错误：服务器接受了无效数据")
            print("=== 测试失败 ===")
            return False
    
    except Exception as e:
        print(f"发生异常: {str(e)}")
        print("=== 测试失败 ===")
        return False

def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) > 1:
        global SERVER_URL
        SERVER_URL = sys.argv[1]
        print(f"使用自定义服务器地址: {SERVER_URL}")
    
    print(f"测试服务器地址: {SERVER_URL}")
    
    # 运行测试
    test_basic_report()
    test_with_female_data()
    test_invalid_data()

if __name__ == "__main__":
    main() 