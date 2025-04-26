from pydantic import BaseModel, Field



'''
paper
'''
class PaperInput(BaseModel):
    paper_info: str = Field(description="사용자 입력 혹은 arxiv url 예시: https://arxiv.org/abs/2210.03629")



'''
weather
'''
class WeatherInput(BaseModel):
    city: str = Field(description="도시 이름 예시: Seoul", default="Seoul")

    
class ClothesInput(BaseModel):
    weather_info: str
