from fastapi import APIRouter, Depends

from users.dao.RedisUtils import get_redis_conn, close_redis_conn
from users.service import HistoryService
from users.utils.JWTDecodeUtils import get_current_user

history_router = APIRouter()
#==========获取历史记录==========
@history_router.get(
    path="/findChatHistory",
    summary="获取历史记录",
    description="获取历史记录",
)
def find_chat_history(current_user: dict = Depends(get_current_user)):
    return HistoryService.find_chat_history(current_user["username"])


#==========具体某一历史记录==========
@history_router.get(
    path="/clickOneConversation",
    summary="点击某一历史记录",
    description="点击某一历史记录",
)
def click_one_conversation(historyId: int,current_user: dict = Depends(get_current_user)):
    return HistoryService.click_one_conversation(current_user["username"],historyId)


#==========删除某一历史记录==========
@history_router.delete(
    path="/deleteChatHistory",
    summary="删除某一历史记录",
    description="删除某一历史记录",
)
def delete_chat_history(historyId: int, current_user: dict = Depends(get_current_user)):
    return HistoryService.delete_chat_history(current_user["username"],historyId)

#=================更改历史记录名称=========
@history_router.put("/renameConversation")
def rename_conversation(historyId:int,newTitle: str,current_user: dict = Depends(get_current_user)):
    # 网上返回同时往下调用到service层
    return HistoryService.rename_conversation(historyId,current_user["username"],newTitle)

@history_router.delete(path="/logout")
def logout(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    r = get_redis_conn()
    try:
        r.delete(f"jwt:{user_id}")
    finally:
        close_redis_conn(r)
    return {
        "code": 200,
        "msg": "退出登录成功"
    }





