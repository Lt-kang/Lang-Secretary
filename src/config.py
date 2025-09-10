import os
from dotenv import load_dotenv
load_dotenv()


import yaml
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")



sqlite3_config = config["sqlite3"]
chroma_config = config["chroma"]
normal_storage_config = config["normal_storage"]


STREAMLIT_PORT = config["port"]["streamlit"]
FASTAPI_PORT = config["port"]["fastapi"]
WEATHER_MCP_PORT = config["port"]["weather_mcp"]

