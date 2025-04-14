#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试脚本：测试飞灵(Fatelling)服务器的基本命盘解读API
"""

import requests
import json
import time
import sys
from rich.console import Console

# 创建Rich控制台
console = Console()

# 服务器地址，可以根据实际情况修改
SERVER_URL = "http://127.0.0.1:8080"  # 默认使用本地服务器地址
API_ENDPOINT = "/api/test"

def test_test_api():
    """测试API服务联通性"""
    print("=== 开始测试API服务联通性 ===")
    try:
        # 发送GET请求
        response = requests.get(f"{SERVER_URL}{API_ENDPOINT}")
        print(f"API响应:")
        console.print(json.dumps(response.json(), ensure_ascii=False, indent=2), style="green")
        response.raise_for_status()  # 如果请求失败，抛出异常
        print("API服务联通性测试成功")
    except requests.exceptions.RequestException as e:
        print(f"API服务联通性测试失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_test_api()
