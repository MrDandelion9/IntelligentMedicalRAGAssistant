import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

# 数据库连接
def get_mysql_conn():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user="Tangl",
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset=os.getenv("MYSQL_CHARSET"),
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
#关闭链接
def close_mysql_conn(cursor,conn):
    cursor.close()
    conn.close()
