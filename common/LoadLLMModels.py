#定义大模型
import os

from langchain_openai import ChatOpenAI


def chatLLM():
    llm_load_model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model=os.getenv("DASHSCOPE_MODEL_NAME"),
)
    return llm_load_model