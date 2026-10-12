from fastapi import APIRouter, Depends

from users.dao.RedisUtils import get_redis_conn, close_redis_conn
from users.service import UsersService
from users.utils.JWTDecodeUtils import get_current_user

users_router = APIRouter()
#创建子路由
@users_router.get(
    path="/sendEmail",
    summary="发送验证码",
    description="发送验证码",
)
def send_email(email: str):
    result = UsersService.send_email(email)
    return result

#验证验证码是否正确
@users_router.get(
    path="/checkCode",
    summary="验证验证码",
    description="验证验证码",
)
def check_code(email: str, code: str):
    return UsersService.check_code(email, code)





