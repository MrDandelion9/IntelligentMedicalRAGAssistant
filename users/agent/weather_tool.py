from langchain_core.tools import tool
from pydantic import BaseModel,Field
import requests


class WeatherTool(BaseModel):
    city: str = Field(..., description="城市名称")

#创建查询天气工具
@tool(
    name_or_callable = "get_weather_tool",
    description="""
           当用户想要询问某个城市的天气时，调用该工具获取天气情况，
           参数：
               city：字符串类型，表示城市名称
       """,
    args_schema=WeatherTool,#参数校验
)
def get_weather_tool(city: str) -> str:
    """
    获取指定城市的天气信息
    """
    # 这里使用天气查询API，请根据实际情况进行替换
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": "b5610f6e96ba4132abf00b8edbb6d1b7",
        "city": city,
    }
    #使用request是方法
    response = requests.get(url, params=params)
    rs = response.json()
    live = rs["lives"][0]
    return (
        f"{live['city']}当前{live['weather']}，"
        f"气温{live['temperature']}°C，"
        f"湿度{live['humidity']}%，"
        f"{live['winddirection']}风{live['windpower']}级，"
        f"更新时间{live['reporttime']}"
    )