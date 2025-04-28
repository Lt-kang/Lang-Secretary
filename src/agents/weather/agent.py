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
        city_weather = response.json()['weather'][0]['description']
        city_wind_speed = response.json()['wind']['speed']
        # return f"현재 {city}의 온도는 {city_temperature}도이고, 날씨는 {city_weather}입니다."
        return f'''검색한 도시: {city}, 온도: {city_temperature}도, 날씨: {city_weather}, 풍속: {city_wind_speed}m/s
        위 네가지 정보는 반드시 사용자에게 알려주고 위 정보를 바탕으로 복장을 함께 추천해주세요.'''
    
    
    except Exception as e:
        print(response.json())
        print("날씨 조회 실패")
        return "날씨 조회 실패"



       

weather_agent_tool = Tool(
    name="weather_tool",
    description="도시명을 입력하면 (온도, 날씨) 정보를 반환합니다. 하지만 아무런 도시명을 말하지 않는다면 함수의 'city' 파라미터의 default 값을 사용합니다. 예: Seoul",
    func=weather_tool,
    args_schema=WeatherInput
    )





weather_tools = [
    weather_agent_tool
]

