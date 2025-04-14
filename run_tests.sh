#!/bin/bash

# 飞灵(Fatelling)服务器测试脚本
# 用于测试服务器API的简单shell脚本

# 设置默认服务器地址
SERVER_URL=${1:-"http://127.0.0.1:8080"}

echo "====================================================="
echo "       飞灵(Fatelling)服务器API测试"
echo "====================================================="
echo "测试服务器地址: $SERVER_URL"
echo "开始测试时间: $(date)"
echo "====================================================="

# 确认Python环境
if ! command -v python3 &> /dev/null
then
    echo "错误: 找不到python3命令，请确认已安装Python"
    exit 1
fi

# 检查依赖
echo "检查必要的Python依赖..."
python3 -c "import requests" 2>/dev/null || { 
    echo "错误: 找不到requests库，正在尝试安装..."
    pip install requests || { 
        echo "安装requests失败，请手动安装: pip install requests"; 
        exit 1; 
    }
}

echo "依赖检查完成，开始运行测试..."
echo "====================================================="

# 运行测试脚本
python3 test_basic_report.py $SERVER_URL

echo "====================================================="
echo "测试完成时间: $(date)"
echo "=====================================================" 