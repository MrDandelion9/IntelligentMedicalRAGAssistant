from fastapi import FastAPI

from users.controller.ChatController import chat_router
from users.controller.HistoryController import history_router
from users.controller.UsersController import users_router

app = FastAPI()
#注册子路由
app.include_router(
    router=users_router,
    prefix="/users",
    tags=["users"],
)

#注册聊天子路由
app.include_router(
    router=chat_router,
    prefix="/chat",
    tags=["chat"],
)

app.include_router(
    router=history_router,
    prefix="/history",
    tags=["history"],
)



#跨域配置
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 允许跨域的源列表
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的请求方法列表
    allow_headers=["*"],  # 允许的请求头列表
)


if __name__ == "__main__":
    #导入uvicorn包来写命令启动fastapi项目服务器
    import uvicorn
    #启动项目文件，即FASTAPI()对象所在的文件
    uvicorn.run(
        app="main:app",#配置启动文件
        host="localhost",#配置启动服务器的ip
        port=8000,#配置启动的服务器端口
        reload=True,#开启自动重启:改代码保存后 uvicorn 自动重载,开发阶段用(上线改回 False)
    )