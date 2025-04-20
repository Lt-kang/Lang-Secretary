from langchain.agents import Tool

import requests
import re


from src.schema.agent_input import ClothesInput, WeatherInput
from src.core.config import OPENWEATHER_CITY, OPENWEATHER_API_KEY




'''
TODO
1.
현재는 openweathermap에서 날씨를 조회하지만
다만 이럴 경우 한국의 경우 서울만 검색이 가능하기에
추후 기상청 api를 활용하도록 수정해야 합니다.

2.
외부 api를 사용하므로 추후 비동기 처리 고려
'''
def weather_tool(city:str = OPENWEATHER_CITY) -> tuple[float, str]:
    if "'" in city:
        city = city.replace("'", "")
    print(f"\n<<<<<<<<<<<<<< {city}의 날씨를 조회합니다. >>>>>>>>>>>>>")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    response = requests.get(api_url)

    try:
        city_temperature = response.json()['main']['temp']
        city_weather = response.json()['weather'][0]['main']
        return f"현재 {city}의 온도는 {city_temperature}도이고, 날씨는 {city_weather}입니다."
    
    except Exception as e:
        print(response.json())
        print("날씨 조회 실패")
        return "날씨 조회 실패"



'''
TODO
복장 추천에 대해 조금 더 세밀하게 추가
'''
def clothes_recommendation(input_text:str) -> str:
    temp, weather = input_text.split(",")
    
    temp_match = re.search(r'[-+]?\d*\.\d+|\d+', temp)
    if temp_match:
        temp = temp_match.group()

    temp = float(temp)
    if temp < 10:
        return "패딩" + " 우산" if "rain" in weather else ""
    elif temp < 20:
        return "가디건" + " 우산" if "rain" in weather else ""
    else:
        return "반팔" + " 우산" if "rain" in weather else ""

       

weather_agent_tool = Tool(
    name="weather_tool",
    description="도시명을 입력하면 (온도, 날씨) 정보를 반환합니다. 하지만 아무런 도시명을 말하지 않는다면 함수의 'city' 파라미터의 default 값을 사용합니다. 예: 'Seoul'",
    func=weather_tool,
    args_schema=WeatherInput
    )


clothes_agent_tool = Tool(
    name="clothes_recommendation",
    description="(온도, 날씨)를 입력하면 복장 추천을 합니다. example output: 패딩",
    func=clothes_recommendation,
    args_schema=ClothesInput
)



weather_tools = [
    weather_agent_tool,
    clothes_agent_tool
]

