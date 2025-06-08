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


# 0. 프로젝트 시작 계기
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

# 1. 프로젝트 개요
해당 프로젝트는 기본적으로 개인화된 비서를 만들고자 하는 생각으로 시작된 프로젝트 입니다.  
그렇기에 제가 자주 사용하는 기능들이 포함되어 있습니다.  

자주 사용하는 기능으로는 `Weather MCP server`와 `Arxiv agent`가 있습니다. 

Weather MCP server의 경우 agent로 구현할 수 있으나 단순 기술 구현을 목적으로 MCP로 구현하였습니다.   
개인적인 사견이지만 특별한 경우가 아니라면 MCP server로 구현하는 것이  
추후 다른 프로젝트에서 MCP server를 재사용하는데 있어서 효과적이라 판단합니다.  

각각의 자세한 기능은 아래에서 설명드리도록 하겠습니다.


___

# 2. 기능 소개
## Weather MCP server
![image](https://github.com/Lt-kang/Lang-Secretary/blob/main/assets/001.png)

국내/외 날씨를 알려주는 MCP server 입니다.  
국내의 경우 세부 명칭 (서울특별시 동작구 등)까지 검색이 가능하며  
알려주는 정보는 실시간 정보 입니다. (정확한 기준 시간은 이미지와 같이 LLM의 출력으로 확인할 수 있습니다.)


## Arxiv Agent
![image](https://github.com/Lt-kang/Lang-Secretary/blob/main/assets/002.png)

Arxiv Agent에 대한 아키텍처는 위 이미지와 같습니다.  
arxiv url에서 arxiv id를 추출한 뒤   
arxiv 라이브러리를 활용하여 로컬에 pdf파일과  
논문 내용을 요약/번역한 파일에 대해 .md 파일을 생성합니다. 

vector db에 저장하는 과정도 있습니다.  
이는 RAG를 고려하여 만든 과정이나  
실제 RAG pipeline을 만들지는 않았습니다.   
(현재 프로젝트에서 RAG 필요성에 대한 의문.)


___


# 3. 기술 스택
- LangChain & LangGraph
- Chroma & Sqlite3
- FastMCP
- streamlit
- docker

___

# 추후 개발(미정)

## 공통
* pytest를 통한 test code 작성
* LangSmith 연동
* MCP server 자율적 추가
* 더 다양한 LLM api 지원 (ex. Claude, Gemini ... )

## Weatehr MCP server
* 정확한 한국어 주소를 찾을 수 있도록 프롬프트 수정
    * 현재는 `OO구`라 입력 받으면 무조건 서울 특별시 내 지역으로 판단함.


## Arxiv Agent
* Arxiv Agent의 출력물을 NotebookLM과 같이 논문 리뷰 팟캐스트 형식으로 tts api를 도입하여 mp4 파일로 생성


