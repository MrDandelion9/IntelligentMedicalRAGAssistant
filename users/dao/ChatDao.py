#数据存入向量库并返回新history_id
from common import MysqlUtils


def save_chat_history(question: str,username: str,parent_id: int,answer: str):
    #链接数据库
    conn = MysqlUtils.get_mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO history (question, username, parent_id, answer, create_time) VALUES (%s, %s, %s, %s, NOW())"
        cursor.execute(sql, (question, username, parent_id, answer))
        conn.commit()  # 提交事务
        return cursor.lastrowid  # 返回新生成的 history_id(自增主键)
    except Exception as e:
        conn.rollback()
        print(f"存入失败{e}")  # 回滚事务
        return None
    finally:
        MysqlUtils.close_mysql_conn(cursor, conn)


