import json

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from users.entity.ConversationEntity import Conversation
from users.service import ChatService
from users.utils.JWTDecodeUtils import get_current_user
from users.utils.JWTDecodeUtils import authenticate_token

#创建聊天子路由
chat_router = APIRouter()
@chat_router.get(
    path="/chat",
    summary="聊天",
    description="与ai聊天",
)
def chat(question: str,historyId: int,token:str):
    current_user = authenticate_token(token)
    username = current_user["username"]
    def generator():
        try:
            for chunk in ChatService.chat(question,historyId, username):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield f"data: {json.dumps({'content': '[END]'})}\n\n"
        except (GeneratorExit, ConnectionResetError, OSError):
            pass

    return StreamingResponse(
        content=generator(),
        media_type="text/event-stream"
    )
#保存历史对话记录
@chat_router.post(
    path="/saveChatHistory",
    summary="保存历史记录",
    description="保存历史记录",
)
def save_chat_history(conversation: Conversation,current_user: dict = Depends(get_current_user)):
    return ChatService.save_chat_history(conversation,current_user["username"])