from common.MysqlUtils import get_mysql_conn, close_mysql_conn



#操作数据库
def check_email(email: str):
   # 获取链接
   conn = get_mysql_conn()
   # 获取游标
   cursor = conn.cursor()
   # 执行sql
   sql = "select * from users where email=%s"
   cursor.execute(sql, [email])
   # 获取结果
   result = cursor.fetchall()
   # 关闭链接
   close_mysql_conn(cursor, conn)
   # 返回结果
   return result


if __name__ == '__main__':
    print(check_email("1494878900@qq.com"))
    #[{'users_id': 1, 'user_name': 'tt', 'email': '1494878900@qq.com', 'create_time': datetime.datetime(2026, 7, 30, 11, 54, 52)}
    #失败返回（）