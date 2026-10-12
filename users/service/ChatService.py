from langchain_core.messages import AIMessageChunk
from common import LoadLLMModels
from common.QueryRewrite import QueryRewriteModel
from users.agent import agent_model
from users.dao import  ChatDao
from users.service import HistoryService
from users.utils import  IntentRecognition


llm = LoadLLMModels.chatLLM()
agent_builder = agent_model.Agent()
agent = agent_builder.get_agent()
def chat(question: str, historyId: int,username: str):
    #保留意图识别，当问题与医疗有关的时候才调用agent来进行调用工具
    if historyId == 0:
        history = []
    else:
        # 判断是否为新对话，如果不是，传入聊天历史记录
        history = HistoryService.click_one_conversation(username,historyId)["data"]

    #使用小模型对用户输入问题进行复写
    rewrite = QueryRewriteModel()
    question = rewrite.query_rewrite(question, history)
    print("重写问题：",{question})
    #使用小模型进行意图识别，如果与医学知识问题无关，就用小模型来回答
    is_medical = IntentRecognition.intentRecognitionModel(question)["is_medical"]
    print("是否调用agent走RAG",is_medical)
    #无关不走RAG，直接大模型回复
    if not is_medical:
        history.append({"role": "user", "content": question})#为小模型也添加历史记录
        for chunk in llm.stream(history):
                yield chunk.content
        return

    #走RAG调用agent
    message = history.copy()
    message.append(({"role": "user", "content": question}))
    print(message)
    #流式输出
    for chunk in agent.stream({"messages": message}, stream_mode="messages"):
        token, metadata = chunk
        if isinstance(token, AIMessageChunk):
            if token.tool_calls:
                print("工具调用结果:",token.tool_calls[0]["name"])
            if token.content:
                yield token.content




#保存对话历史
def save_chat_history(conversation,username: str):
    question = conversation.question
    parent_id = conversation.parent_id
    answer = conversation.answer
    #存入数据库，获取新的history_id
    history_id=ChatDao.save_chat_history(question,username,parent_id,answer)
    if history_id:
        return{
            "code": 200,
            "msg": "保存成功",
            "data":history_id
        }
    return {
        "code": 500,
        "msg": "保存失败",
        "data": None
    }




if __name__ == '__main__':
    # for chunk in chat("我肚子痛有什么可能"):
    #     print(chunk)
    for chunk in chat("糖尿病的并发症", 0, "tt"):
        if chunk:
            print(chunk.strip())