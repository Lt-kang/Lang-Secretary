from dotenv import load_dotenv
import os

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경 변수 읽기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
STUDY_DB_PATH = os.getenv("STUDY_DB_PATH")


