from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
import requests
from pydantic import BaseModel

from src.chains.llm_regeistry import weather_llm
from src.config import OPENWEATHER_CITY, OPENWEATHER_API_KEY


apikey = OPENWEATHER_API_KEY
lang = "kr"

'''
현재는 openweathermap에서 날씨를 조회합니다.
다만 이럴 경우 한국의 경우 서울만 검색이 가능하기에
추후 기상청 api를 활용하도록 수정해야 합니다.
'''
def weather_tool(city:str = OPENWEATHER_CITY) -> str:
    if "'" in city:
        city = city.replace("'", "")
    print(f"<<<<<<<<<<<<<< {city}의 날씨를 조회합니다. >>>>>>>>>>>>>")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric&lang={lang}"
    response = requests.get(api_url)
    try:
        city_temperature = response.json()['main']['temp']
        city_weather = response.json()['weather'][0]['main']
        return (city_temperature, city_weather)
    except Exception as e:
        print(response.json())
        print("날씨 조회 실패")
        return "날씨 조회 실패"


class WeatherInput(BaseModel):
    city: str


tools = [Tool(
    name="weather_tool",
    description="도시명을 입력하면 (온도, 날씨) 정보를 반환합니다. 하지만 아무런 도시명을 말하지 않는다면 함수의 'city' 파라미터의 default 값을 사용합니다. 예: 'Seoul'",
    func=weather_tool,
    args_schema=WeatherInput
    )
]


weather_agent_executor = initialize_agent(
    tools=tools,
    llm=weather_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    response = weather_agent_executor.invoke({"input": "오늘 날씨 알려줘"})
    print(response)
    

''' api 응답 예시
{
    "coord": {
        "lon": 126.9778,
        "lat": 37.5683
    },
    "weather": [
        {
            "id": 501,
            "main": "Rain",
            "description": "보통 비",
            "icon": "10d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 5.95,
        "feels_like": 2.93,
        "temp_min": 5.95,
        "temp_max": 5.95,
        "pressure": 996,
        "humidity": 76,
        "sea_level": 996,
        "grnd_level": 986
    },
    "visibility": 10000,
    "wind": {
        "speed": 4.17,
        "deg": 74,
        "gust": 6.05
    },
    "rain": {
        "1h": 1.78
    },
    "clouds": {
        "all": 100
    },
    "dt": 1744614919,
    "sys": {
        "country": "KR",
        "sunrise": 1744577930,
        "sunset": 1744625135
    },
    "timezone": 32400,
    "id": 1835848,
    "name": "Seoul",
    "cod": 200
}
'''