from dotenv import load_dotenv
import os

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경 변수 읽기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
STUDY_DB_PATH = os.getenv("STUDY_DB_PATH")

OPENWEATHER_CITY = os.getenv("OPENWEATHER_CITY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

VERBOSE = True if os.getenv("VERBOSE")=="1" else False

PAPER_SAVE_DIR = os.getenv("PAPER_SAVE_DIR")
os.makedirs(PAPER_SAVE_DIR, exist_ok=True)

ENV = os.getenv("ENV")
