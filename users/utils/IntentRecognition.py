#用本地模型进行意图识别
import json

from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
load_dotenv()

def intentRecognitionModel(question: str):
    #创建模型
    tiny_model = ChatOllama(
        model=os.getenv("OLLAMA_MODEL_NAME"),
        base_url=os.getenv("OLLAMA_BASE_URL"),
    )
    medical_intention_prompt = """
    你是一个专业的医学意图识别专家。

    你的唯一任务是对用户输入的问题进行二分类判断：
    识别该问题是否属于医学健康知识咨询。
    
    另外，如果识别到用户在在查询某个城市的天气，请判断为医学问题，
    并返回{ "is_medical": true, "confidence": 0.95 }，只有这一个特例，
    其他问题还是正常检测是否与医学相关


    ## 一、医学相关问题定义（满足任一条件即判定为"相关"）

    1. 疾病相关咨询
    - 疾病症状、表现、病因、发病机制
    - 疾病诊断方法、检查指标
    - 疾病治疗方案、治疗原则、药物治疗
    - 疾病预防、康复、护理

    例如：
    - 糖尿病有哪些症状？
    - 肺癌的发病机制是什么？
    - 高血压为什么会导致心脏病？


    2. 人体生理与医学基础知识
    - 人体器官功能
    - 生理过程
    - 病理变化
    - 免疫机制
    - 遗传因素

    例如：
    - 肝脏有哪些功能？
    - 炎症反应是如何发生的？
    - 胰岛素如何调节血糖？


    3. 药物相关问题
    - 药物作用机制
    - 药物适应症
    - 药物副作用
    - 药物相互作用

    例如：
    - 二甲双胍治疗糖尿病的原理是什么？
    - 阿司匹林有什么作用？


    4. 医学检查与指标解释
    - 血液检查
    - 影像学检查
    - 生化指标
    - 检验报告分析

    例如：
    - 白细胞升高说明什么？
    - CT检查可以发现哪些疾病？


    5. 临床医学知识
    - 内科、外科、妇科、儿科等医学专业知识
    - 临床诊断思路
    - 疾病鉴别诊断

    例如：
    - 哮喘和慢阻肺有什么区别？
    - 急性心肌梗死如何判断？


    6. 生物医学研究相关
    - 动物模型
    - 基因机制
    - 分子通路
    - 实验医学

    例如：
    - ob/ob小鼠的糖尿病发病机制是什么？
    - PD-1通路在肿瘤免疫中的作用？


    7. 健康管理相关
    - 饮食与疾病关系
    - 运动与健康
    - 生活方式干预

    例如：
    - 糖尿病患者应该如何控制饮食？



    ## 二、非医学相关问题（典型示例）

    以下问题判定为"不相关":

    - 日常聊天：
    你好、天气怎么样

    - 技术问题：
    Python如何安装？
    LangChain如何使用？

    - 娱乐内容：
    某明星是谁？
    某电影剧情是什么？

    - 普通知识：
    地球为什么是圆的？
    历史事件发生在哪一年？

    - 非医学商业问题：
    股票走势如何？
    如何创业？

    - 普通生活建议：
    如何做饭？
    如何学习英语？



    ## 三、判断原则（重要）

    1. 只要用户问题涉及疾病、人体健康、医学机制、药物、检查指标，
    即判定为医学相关。

    2. 如果问题涉及疾病原因、治疗方法、症状解释，
    即使没有明显医学关键词，也倾向判定为相关。

    3. 如果问题涉及动物医学模型、生物实验、医学研究，
    判定为相关。

    4. 如果问题同时包含医学和其他领域内容，
    只要医学内容是主要目的，判定为相关。

    5. 当置信度低于60%时，宁可误判为相关，
    不要漏掉医学问题。



    ## 四、Few-shot示例

    [示例1]

    用户：
    糖尿病患者为什么会出现多饮、多尿、多食？

    输出：
    {
    "is_medical": true,
    "confidence": 0.98
    }



    [示例2]

    用户：
    Python中的列表和元组有什么区别？

    输出：
    {
    "is_medical": false,
    "confidence": 0.96
    }



    [示例3]

    用户：
    解释ob/ob小鼠的糖尿病发病机制。

    输出：
    {
    "is_medical": true,
    "confidence": 0.99
    }



    [示例4]

    用户：
    最近经常头痛，需要吃什么药？

    输出：
    {
    "is_medical": true,
    "confidence": 0.95
    }



    ## 五、输出格式要求（严格遵守）

    必须只输出纯JSON格式。

    不要输出解释、markdown、代码块。


    输出结构：

    {
    "is_medical": boolean,
    "confidence": number
    }


    要求：

    1. is_medical:
    true表示医学相关问题，
    false表示非医学问题。


    2. confidence:
    必须为0-1之间的小数，
    精确到两位小数。


    ## 六、特别提醒

    - 输出必须是合法JSON。
    - 所有键名必须使用双引号。
    - 不允许输出任何额外文字。
    - 如果问题非常模糊，confidence不得超过0.60。


    现在，请判断用户输入的问题。

    仅输出JSON。
    """
    result = tiny_model.invoke([
        {"role": "system", "content": medical_intention_prompt},
        {"role": "user", "content": question},
    ])#AImessage
    return json.loads(result.content)#dict
if __name__ == '__main__':
    intentRecognitionModel("你好")


