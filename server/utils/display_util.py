from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.markdown import Markdown
from typing import Any, Dict, Optional

console = Console()
print(f"console size: ({console.width}, {console.height})")

def format_duration(nanoseconds: int, total: Optional[int] = None) -> str:
    """将纳秒转换为可读时间格式，如果提供total则计算百分比"""
    milliseconds = nanoseconds / 1_000_000
    if total:
        percentage = (nanoseconds / total) * 100
        return f"{milliseconds:.2f}ms ({percentage:.1f}%)"
    return f"{milliseconds:.2f}ms"

def add_response_meta_info(table: Table, metadata: Dict[str, Any]):
    # 基本信息
    table.add_row("模型", metadata.get('model', 'unknown'))
    table.add_row("创建时间", metadata.get('created_at', 'unknown'))
    table.add_row("完成状态", "已完成" if metadata.get('done', False) else "未完成")
    table.add_row("完成原因", metadata.get('done_reason', 'unknown'))
    
    # 添加分隔空行
    table.add_row("", "")
    
    # 性能指标
    total_time = metadata.get('total_duration', 0)
    table.add_row("总耗时", format_duration(total_time))
    table.add_row("模型加载时间", format_duration(metadata.get('load_duration', 0), total_time))
    table.add_row("提示词评估时间", format_duration(metadata.get('prompt_eval_duration', 0), total_time))
    table.add_row("生成评估时间", format_duration(metadata.get('eval_duration', 0), total_time))
    
    # 计算其他时间（总时间减去已知时间）
    known_time = (metadata.get('load_duration', 0) + 
                 metadata.get('prompt_eval_duration', 0) + 
                 metadata.get('eval_duration', 0))
    other_time = total_time - known_time
    if other_time > 0:
        table.add_row("其他处理时间", format_duration(other_time, total_time))
    
    # 添加分隔空行
    table.add_row("", "")
    
    # 处理统计
    table.add_row("提示词评估次数", str(metadata.get('prompt_eval_count', 0)))
    table.add_row("生成评估次数", str(metadata.get('eval_count', 0)))
    
    # 计算每次评估的平均时间
    if metadata.get('prompt_eval_count', 0) > 0:
        avg_prompt_time = metadata.get('prompt_eval_duration', 0) / metadata.get('prompt_eval_count', 1)
        table.add_row("平均提示词评估时间", format_duration(int(avg_prompt_time)))
    
    if metadata.get('eval_count', 0) > 0:
        avg_eval_time = metadata.get('eval_duration', 0) / metadata.get('eval_count', 1)
        table.add_row("平均生成评估时间", format_duration(int(avg_eval_time)))
    
    # 计算生成速度
    if metadata.get('eval_count', 0) > 0 and metadata.get('eval_duration', 0) > 0:
        # 将纳秒转换为秒
        eval_duration_seconds = metadata.get('eval_duration', 0) / 1_000_000_000
        generation_speed = metadata.get('eval_count', 0) / eval_duration_seconds
        table.add_row("生成速度", f"{generation_speed:.1f} tokens/s")
    
    # 消息信息
    message = metadata.get('message', {})
    if isinstance(message, dict):
        table.add_row("", "")
        table.add_row("消息角色", message.get('role', 'unknown'))
        table.add_row("包含图片", "是" if message.get('images', None) else "否")
        table.add_row("包含工具调用", "是" if message.get('tool_calls', None) else "否")
    

def add_usage_meta_info(table: Table, metadata: Dict[str, Any]):
    """添加令牌使用信息到表格
    
    Args:
        table: 要添加信息的表格
        metadata: 包含令牌使用信息的元数据
    """
    if not metadata:
        return
        
    # 添加分隔空行
    
    # 添加令牌使用信息
    table.add_row("输入tokens", str(metadata.get('input_tokens', 0)))
    table.add_row("输出tokens", str(metadata.get('output_tokens', 0)))
    table.add_row("全部tokens", str(metadata.get('total_tokens', 0)))


def display_model_response(content: str, response_metadata: Dict[str, Any], usage_metadata: Optional[Dict[str, Any]] = None, debug: bool = False) -> None:
    """显示模型响应和相关信息
    
    Args:
        content: 模型的响应内容
        response_metadata: 响应的元数据
        usage_metadata: 令牌使用的元数据（可选）
        debug: 是否显示调试信息
    """
    if debug:
        console.print("\n[dim]Debug: Response Metadata Structure:[/dim]")
        console.print(response_metadata)
        if usage_metadata:
            console.print("\n[dim]Debug: Usage Metadata Structure:[/dim]")
            console.print(usage_metadata)
    
    # 使用Markdown渲染模型响应
    md = Markdown(content)
    console.print(Panel(
        md,
        title="[bold magenta]模型响应[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
        expand=False,
    ))
    
    # 创建信息表格
    table = Table(box=None, show_header=False, show_edge=False, pad_edge=False, padding=(0, 4))
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="green")

    add_response_meta_info(table, response_metadata)
    table.add_row("", "")
    add_usage_meta_info(table, usage_metadata)

    console.print(Panel(
        table,
        title="[bold cyan]模型运行信息[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
        expand=False,
    ))
