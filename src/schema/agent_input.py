from pydantic import BaseModel



'''
paper
'''
class PaperInput(BaseModel):
    paper_title: str
    paper_url: str


'''
weather
'''
class WeatherInput(BaseModel):
    city: str

    
class ClothesInput(BaseModel):
    weather_info: str
