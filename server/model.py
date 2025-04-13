import os
from dotenv import load_dotenv

from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama


"""
开发中可用的模型类型
"""
MODEL_SOURCE = [
    "aliyun", # 阿里云百炼
    "local",  # 公司内部模型 or Mac本地模型 (Ollama)
]

def get_aliyun_chat_model():
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = os.getenv('ALIYUN_API_KEY')
    
    if not api_key:
        print("错误：未找到API密钥。请确保.env文件中包含ALIYUN_API_KEY。")
        raise ValueError("未找到API密钥。请确保.env文件中包含ALIYUN_API_KEY。")
    
    # 配置ChatOpenAI
    return ChatOpenAI(
        model_name      = "deepseek-r1",
        openai_api_key  = api_key,
        openai_api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature     = 0
    )


def get_ollama_chat_model():
    import platform
    REMOTE_HOST = "192.168.11.8" if platform.system() == "Linux" else "127.0.0.1"
    OLLAMA_PORT = 11434

    return ChatOllama(
        base_url    = f"http://{REMOTE_HOST}:{OLLAMA_PORT}",
        model       = "deepseek-r1:8b",
        temperature = 0.7,
        timeout     = 30
    )


def get_chat_model(model_source: str):
    if model_source == "aliyun":
        return get_aliyun_chat_model()
    elif model_source == "local":
        return get_ollama_chat_model()
    else:
        raise ValueError(f"未找到模型类型: {model_source}")


__all__ = ["get_chat_model"]