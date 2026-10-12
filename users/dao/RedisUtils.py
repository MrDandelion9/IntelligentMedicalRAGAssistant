import os

import redis
from dotenv import load_dotenv
load_dotenv()

def get_redis_conn():
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=int(os.getenv("REDIS_DB")),
        protocol=2,
        decode_responses=True,#将byte转化为字符串，方便后续对比
    )
def close_redis_conn(conn):
    conn.close()
