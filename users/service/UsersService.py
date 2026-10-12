import os
import smtplib
from email.mime.text import MIMEText
import random
from users.dao.RedisUtils import get_redis_conn, close_redis_conn
from dotenv import load_dotenv

from users.utils.SecretKeyUtils import create_access_token

load_dotenv()
from users.dao import UsersDao

def send_email(email: str):
    #需要检查数据库中是否注册过该邮箱
    mark=False
    result = UsersDao.check_email(email)
    #获取该邮箱名是否存在，若存在再发送，使用isinstance函数判断是否
    if isinstance(result, list):
        username = result[0]["user_name"]
        mark=True
    if not mark:
        #此时不发送
        return{
            "code":500,
            "msg":"邮箱号未注册",
            "data":None
        }
    code = ""  # 随机四位验证码
    for i in range(4):
        code += str(int(random.random() * 10))
    #使用MIME
    #配置发送信息
    sender = os.getenv("SENDER_EMAIL")
    sender_pwd = os.getenv("SENDER_EMAIL_PASSWORD")
    subject = "登录验证码来了，请注意查收"
    content = f"你的验证码为：{code}, 【请注意】：过期时间为：60s"
    message = MIMEText(content, "plain", "utf-8")
    # 添加内容在message中
    message["From"] = sender
    message["To"] = email
    message["Subject"] = subject
    #使用smtp发送邮件
    try:
        # 构建发送邮件的对象
        smtp = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
        # 开启邮件发送服务 TLS
        smtp.starttls()
        # 验证发送方和发送方的授权码是否能对上
        smtp.login(sender, sender_pwd)
        # 发送邮件 -- sendmail 发送邮件的方法：发送方，接收方，邮件对象
        smtp.sendmail(sender, email, message.as_string())
        smtp.quit()
        # 把验证码存入到redis中
        r = get_redis_conn()
        # redis存入数据通过key,value格式 --- 取值通过key
        r.setex(email, 60, code)  # 60秒后过期，key:email value:code
        close_redis_conn(r)
        return {
            "code": 200,
            "msg": "发送成功",
            "data": username
        }
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return {
            "code": 500,
            "msg": "发送邮件失败",
            "data": None
        }

#验证验证码，通过邮箱当作k值来判断code
def check_code(email: str, code: str):
    #链接redis
    r = get_redis_conn()
    redis_code = r.get(email)
    try:
        if redis_code == None:
            return {
                "code": 500,
                "msg": "验证码已过期",
                "data": None
            }
        if redis_code == code:
            user = UsersDao.check_email(email)
            if not user:
                return {
                    "code": 500,
                    "msg": "用户不存在",
                    "data": None
                }
            user_id = user[0]["users_id"]
            username = user[0]["user_name"]
            #s生成token
            token = create_access_token({"user_id": user_id, "username": username})
            #存入redis中
            r.setex(f"jwt:{user_id}", int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60, token)
            return {
                "code": 200,
                "msg": "验证成功",
                "data": token
            }
        else:
            return {
                "code": 500,
                "msg": "验证失败",
                "data": None
            }
    except Exception as e:
        print(f"验证码验证失败: {e}")
        return {
            "code": 500,
            "msg": "验证码验证失败",
            "data": None
        }
    finally:
        #关闭redis链接
        close_redis_conn(r)



if __name__ == '__main__':
    result=check_code("1494878900@qq.com", "1234")
    print(result["data"])
    #token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InR0IiwiZXhwIjoxNzg2NzY3MDY5LCJpYXQiOjE3ODY3NjcwMDl9.NSUjoqlE3yXT5-2YW-xKu3Pfvpquk4-IsQeKxmIroEw'}

