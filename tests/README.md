# 飞灵服务器测试指南

本文档介绍如何运行和管理飞灵（Fatelling）服务器的测试用例。

## 环境准备

1. 安装项目依赖：
```bash
# 在项目根目录下执行
pip install -r requirements.txt
```

2. 安装项目（开发模式）：
```bash
# 在项目根目录下执行
pip install -e .
```

## 运行测试

### 运行所有测试
```bash
# 在项目根目录下执行
pytest tests/test_api.py -v
```

### 运行特定测试
```bash
# 运行特定的测试函数
pytest tests/test_api.py::test_calculate_bazi -v

# 运行包含特定名称的测试
pytest -k "basic" -v  # 运行所有包含 "basic" 的测试
```

### 生成测试报告
```bash
# 生成HTML格式的测试报告（需要安装 pytest-html 插件）
pytest tests/test_api.py -v --html=report.html --self-contained-html
```

测试报告会生成在当前目录下的 `report.html` 文件中，包含了详细的测试结果、覆盖率和失败信息。使用 `--self-contained-html` 参数可以生成一个独立的 HTML 文件，不依赖外部资源。

## 测试用例说明

目前包含以下测试用例：

1. `test_test_api`: 测试API服务联通性
2. `test_calculate_bazi`: 测试八字计算API
3. `test_basic_report`: 测试基本命盘解读API
4. `test_fate_report`: 测试流式命理报告API
5. `test_invalid_input`: 测试无效输入的错误处理

## 添加新的测试

1. 在 `tests/test_api.py` 文件中添加新的测试函数
2. 测试函数名必须以 `test_` 开头
3. 使用 `test_client` fixture 来发送请求
4. 使用 `assert` 语句验证结果

示例：
```python
def test_new_feature(test_client):
    """测试新功能"""
    response = test_client.post("/api/new_feature", json={
        "param1": "value1",
        "param2": "value2"
    })
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

## 调试测试

### 查看详细输出
```bash
pytest -v --capture=no tests/test_api.py
```

### 调试失败的测试
```bash
# 在失败时立即停止
pytest -x tests/test_api.py

# 显示失败测试的完整回溯
pytest --tb=long tests/test_api.py
```

### 并行运行测试
```bash
pytest -n auto tests/test_api.py
```

## 最佳实践

1. 每个测试函数应该只测试一个功能点
2. 使用有意义的测试函数名称
3. 添加清晰的文档字符串
4. 测试正常情况和边界情况
5. 使用 fixture 复用测试代码
6. 保持测试代码的简洁和可维护性

## 常见问题解决

1. 模块导入错误
   - 确保已经在开发模式下安装了项目 (`pip install -e .`)
   - 检查 `PYTHONPATH` 是否正确设置

2. 环境变量问题
   - 创建 `.env` 文件设置必要的环境变量
   - 或在运行测试前设置环境变量：
     ```bash
     export MODEL_SOURCE=local
     pytest tests/test_api.py
     ```

3. 依赖服务问题
   - 确保所有必要的外部服务（如 LLM 模型）已经启动
   - 检查服务连接配置是否正确

## 持续集成

建议配置 GitHub Actions 或其他 CI 工具来自动运行测试：

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      - name: Run tests
        run: |
          pytest tests/test_api.py -v
``` 