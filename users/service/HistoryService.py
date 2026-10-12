#获取history_id对应的question历史记录
from users.dao import HistoryDao

#============获取历史记录============
def find_chat_history(username):

    chat_list = []
    results = HistoryDao.find_chat_history(username)
    for result in results:
        chat_list.append({
            "historyId": result["history_id"],
            "title": result["question"],
            "time": result['create_time'].strftime("%Y-%m-%d %H:%M:%S"),
        })
    return {
        "code": 200,
        "msg": "获取成功",
        "data": chat_list
    }

#===========获取某一历史记录============
def click_one_conversation(username: str,historyId: int):
    results = HistoryDao.click_one_conversation(username ,historyId)
    results_list = []
    for item in results:
        results_list.append({
            "role": "user",
            "content": item['question'],
        })
        results_list.append({
            "role": "assistant",
            "content": item['answer'],
        })
    if results:
        return {
            "code": 200,
            "msg": "获取成功",
            "data": results_list
        }
    return {
        "code": 500,
        "msg": "获取失败",
        "data": None
    }

#===========删除某一历史聊天记录============
def delete_chat_history(username: str,historyId: int):
    if HistoryDao.delete_chat_history(username,historyId):
        return {
            "code": 200,
            "msg": "删除成功",
            "data": None
        }


def rename_conversation(historyId:int,username: str,newTitle: str):
    result = HistoryDao.rename_conversation(historyId,username,newTitle)#这里是继续往下调用
    if result:
        return {
            "code": 200,
            "msg": "修改成功",
            "data": result
        }#这里是往上返回数据到controller层
    return {
        "code": 500,
        "msg": "修改失败",
        "data": None
    }

