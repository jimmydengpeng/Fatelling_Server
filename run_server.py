import uvicorn
from server.app import app
import argparse
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--local", action="store_true", help="使用本地部署的模型")
    group.add_argument("--api", action="store_true", help="使用API访问远端模型")
    args = parser.parse_args()
    
    # 创建Rich控制台
    console = Console()
    
    # 根据命令行参数设置环境变量
    model_msg = ""
    if args.local:
        os.environ["MODEL_SOURCE"] = "local"
        model_msg = "本地"
    elif args.api:
        os.environ["MODEL_SOURCE"] = "aliyun"
        model_msg = "远端"
    else:
        # 默认使用本地模式
        os.environ["MODEL_SOURCE"] = "local"
        model_msg = "本地"
    
    # 加载环境变量
    load_dotenv()
    
    # 创建面板内容
    panel_content = Text()
    panel_content.append("模型配置: ", style="bold cyan")
    panel_content.append(f"{model_msg}\n", style="green")
    panel_content.append("系统地址: ", style="bold cyan")
    panel_content.append("http://localhost:8080\n", style="blue underline")
    panel_content.append("文档地址: ", style="bold cyan")
    panel_content.append("http://localhost:8080/docs", style="blue underline")
    
    # 显示面板
    console.print(Panel(
        panel_content,
        title="飞灵（Fatelling）- AI智能命运决策助手",
        subtitle="服务启动成功",
        border_style="bright_green",
        expand=False,
        padding=(1, 2)
    ))
    
    # 启动服务器
    uvicorn.run(app, host="0.0.0.0", port=8080)