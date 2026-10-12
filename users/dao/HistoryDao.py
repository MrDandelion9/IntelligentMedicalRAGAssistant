
from common import MysqlUtils


def find_chat_history(username):
    sql = "SELECT history_id,question,create_time FROM history WHERE parent_id=0 and username = %s "
    conn = MysqlUtils.get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, (username,))
        results = cur.fetchall()
        if results:
            return results
        else:
            return None
    except Exception as e:
        print(f"获取失败{e}")
        return None
    finally:
        MysqlUtils.close_mysql_conn(cur, conn)


def click_one_conversation(username: str,historyId: int):
    sql="SELECT history_id,question,answer FROM history WHERE username=%s AND (history_id=%s OR parent_id=%s) ORDER BY history_id ASC"
    conn = MysqlUtils.get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, (username, historyId, historyId))
        results = cur.fetchall()
        if results:
            return results
        return None
    except Exception as e:
        print(f"错误：{e}")
        return None
    finally:
        MysqlUtils.close_mysql_conn(cur, conn)



def delete_chat_history(username: str,historyId: int):
    sql = "DELETE FROM history WHERE username = %s and (history_id=%s or parent_id=%s)"
    conn = MysqlUtils.get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, (username,historyId,historyId))
        conn.commit()
        return True
    except Exception as e:
        print(f"删除失败{e}")
        conn.rollback()
        return False
    finally:
        MysqlUtils.close_mysql_conn(cur, conn)


def rename_conversation(historyId:int,username: str,newTitle: str):
    conn = MysqlUtils.get_mysql_conn()
    cur = conn.cursor()
    try:

        sql = "UPDATE history SET question=%s WHERE history_id=%s AND parent_id=0 And username=%s ;"
        cur.execute(sql, [newTitle,historyId, username])
        conn.commit ()
        return cur.rowcount
    except  Exception as e:
        conn.rollback()
        print(f"修改失败{e}")
        return None
    finally:
        MysqlUtils.close_mysql_conn(cur, conn)



