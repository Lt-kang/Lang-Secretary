from dotenv import load_dotenv
import os

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경 변수 읽기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./db/default_vector.db")
NORMAL_DB_PATH = os.getenv("NORMAL_DB_PATH", "./db/default_normal.db")
ENV = os.getenv("ENV", "development")

# # LangChain에서 사용할 LLM 관련 기본 설정도 여기에 모을 수 있음
# DEFAULT_TEMPERATURE = 0.7
# MAX_TOKENS = 2048
