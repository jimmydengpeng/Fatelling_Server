#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试文件：使用pytest测试飞灵(Fatelling)服务器的所有API接口
"""

import pytest
from fastapi.testclient import TestClient
from server.app import app
from server.fate_owner import Gender
import json

# 创建测试客户端
client = TestClient(app)

# 测试数据
test_birth_info = {
    "year": 1990,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 0,
    "gender": "male",
    "timezone": 8
}

@pytest.fixture
def test_client():
    """创建测试客户端的fixture"""
    return client

def test_test_api(test_client):
    """测试API服务联通性"""
    response = test_client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is working"}

def test_calculate_bazi(test_client):
    """测试八字计算API"""
    response = test_client.post("/api/calculate_bazi", json=test_birth_info)
    assert response.status_code == 200
    data = response.json()
    assert "bazi_string" in data
    assert "five_elements" in data
    assert "pillars" in data

def test_basic_report(test_client):
    """测试基本命盘解读API"""
    response = test_client.post("/api/basic_report", json=test_birth_info)
    assert response.status_code == 200
    data = response.json()
    assert "bazi" in data
    assert "reading" in data

def test_fate_report(test_client):
    """测试流式命理报告API"""
    # 测试POST方法
    response = test_client.post("/api/fate_report", json=test_birth_info)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
    
    # 测试GET方法
    response = test_client.get(f"/api/fate_report?data={json.dumps(test_birth_info)}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"

def test_invalid_input(test_client):
    """测试无效输入的错误处理"""
    invalid_data = {
        "year": 2025,  # 未来年份
        "month": 13,   # 无效月份
        "day": 1,
        "hour": 12,
        "minute": 0,
        "gender": "invalid",
        "timezone": 8
    }
    response = test_client.post("/api/calculate_bazi", json=invalid_data)
    assert response.status_code == 422  # FastAPI的验证错误状态码

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 