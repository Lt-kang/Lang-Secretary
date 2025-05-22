# 0. 프로젝트 개요
해당 프로젝트는 모 중소기업에 ai agent 개발자 직무에 면접을 보러갔다가   
자신의 능력에 대해 부족함을 깨닫고 제대로 된 개발을 해보자는 취지해서 시작함.  

면접에서 느낀 나의 부족함은 크게 세가지  
첫번째, `프로젝트 설계`에 대한 지식 부족  
두번째, 구현에만 신경 쓰며 이걸 왜 만드는지에 대한 `문제 정의 및 해결`에는 등한시  
세번째, 만들고자 하는 앱(혹은 모델)에 대해서 `정확한 목표 스펙` 미설정  

나의 개발 실력이 부족한 만큼.  
해당 프로젝트로 성장하려는 것이 목표이며 동시에   
나의 성장을 도와줄 훌륭한 agent를 만드는게 목표이며  
동시에 나와 같이 비전공으로 시작하여 개발자의 꿈을 꾸는 사람들에게  
도움이 되기를 바라는 마음에 해당 프로젝트를 시작함.

___
## 실행 환경
```
window 10
python 3.11.5
```

## 실행 방법

### 1. python package 설치
```
python -m pip install -r requirements.txt
```

### 2. .env 설정
```
.env.example 참조
```

### 3. api server 실행
```
python -m src.mcp_server.weather.weather_mcp_sse
python -m src.run_api
```

### 4. frontend server 실행  
```
python -m streamlit run ./src/run_streamlit.py
```
___

# 1. 기술 스택
- LangGraph: route 기반 대화 구현 목적
- Chroma & Sqlite3: vertor db 및 local db
- FastMCP: MCP server 구현
- streamlit: front-end 구현
- docker: 배포
___



