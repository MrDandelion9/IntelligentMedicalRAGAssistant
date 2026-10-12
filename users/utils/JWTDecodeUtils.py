from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError

from users.dao.RedisUtils import get_redis_conn, close_redis_conn
from users.utils.SecretKeyUtils import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def authenticate_token(token: str) -> dict:
    try:
        payload = verify_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token已过期")
    except JWTError:
        raise HTTPException(status_code=401, detail="token无效")

    user_id = payload.get("user_id")
    username = payload.get("username")
    r = get_redis_conn()
    try:
        stored_token = r.get(f"jwt:{user_id}")
        if stored_token != token:
            raise HTTPException(status_code=401, detail="请先登录")
    finally:
        close_redis_conn(r)
    return {"user_id": user_id, "username": username}

def get_current_user(token: str = Depends(oauth2_scheme)):
    return authenticate_token(token)





if __name__ == '__main__':
    # result = check_code("1494878900@qq.com", "1234")
    # print(result)
    # token = result["data"]
    #print(token)
    print(get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InR0IiwiZXhwIjoxNzg2Nzc1MzU4LCJpYXQiOjE3ODY3NzM1NTh9.VdAiDkEPD_FZDlEDId33ZAX9jAAXwnQNz6m25OpwbHY"))