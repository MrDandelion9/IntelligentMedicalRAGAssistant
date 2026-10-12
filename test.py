from langchain_core.messages import AIMessageChunk
from common import LoadLLMModels
from users.agent import agent_model
from users.service import HistoryService
from users.utils import  IntentRecognition
from users.utils.logger import Logger

llm = LoadLLMModels.chatLLM()
agent_builder = agent_model.Agent()



logger = Logger.get_logger(__name__)
class Chat:
    def __init__(self):
        logger.info("初始化大语言模型")
        self.llm = LoadLLMModels.chatLLM()

    def chat(self, question: str, historyId: int,username: str):
        try:
            logger.info("开始处理用户问题: %s", question)
            # 保留意图识别，当问题与医疗有关的时候才调用agent来进行调用工具
            if historyId == 0:
                history = []
            else:
                # 判断是否为新对话，如果不是，传入聊天历史记录
                history = HistoryService.click_one_conversation(username, historyId)["data"]
            # 使用小模型进行意图识别，如果与医学知识问题无关，就用小模型来回答
            is_medical = IntentRecognition.intentRecognitionModel(question)["is_medical"]
            logger.info("是否调用agent走RAG: %s", is_medical)
            # 无关不走RAG，直接大模型回复
            if not is_medical:
                history.append({"role": "user", "content": question})  # 为小模型也添加历史记录
                for chunk in self.llm.stream(history):
                    yield chunk.content
                return

            # 走RAG调用agent
            message = history.copy()
            message.append(({"role": "user", "content": question}))
            logger.info("输入给agent的消息: %s", message)
            # 流式输出
            agent = agent_builder.get_agent()
            for chunk in agent.stream({"messages": message}, stream_mode="messages"):
                token, metadata = chunk
                if isinstance(token, AIMessageChunk):
                    if token.tool_calls:
                        logger.info("工具调用结果: %s ", token.tool_calls[0]["name"])
                    if token.content:
                        yield token.content
        except Exception as e:
            logger.error(f"聊天失败：{e}")
chat_func = Chat()
if __name__ == '__main__':
    # for chunk in chat("我肚子痛有什么可能"):
    #     print(chunk)
    for chunk in chat_func.chat("糖尿病的并发症", 0, "tt"):
        if chunk:
            print(chunk.strip())