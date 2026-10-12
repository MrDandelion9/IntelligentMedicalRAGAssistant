from datetime import datetime, timedelta, timezone
import os
import secrets

from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv()

# 生成32位密钥
def key():
    key =  secrets.token_urlsafe(32)
    print(key)#mdPVmEdGW5h8dMrkNQgKTq5GXpPW9oHTF9Pgdw337Xo

def create_access_token(data: dict) -> str:
    # 拷贝一份data
    copy_data = data.copy()
    # 设置token到什么时间过期 = 当前时间 + 设置的过期时间
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    # 修改copy_data数据，添加过期时间 --- exp: 过期时间, iat: token生成时间
    copy_data.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    # 生成token
    return jwt.encode(
        claims=copy_data,  # 数据
        key=os.getenv("SECRET_KEY"),  # 密钥
        algorithm=os.getenv("ALGORITHM"),  # 算法
    )

# 验证token
def verify_token(token: str) -> dict:
    return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])