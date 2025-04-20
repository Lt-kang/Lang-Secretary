import streamlit as st
import requests


from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")

if ENV == "dev":
    backend_url = "http://localhost:8000"
else:
    backend_url = "http://lang-backend:8000"

st.set_page_config(page_title="Lang-Secretary", page_icon=":shark:")
st.title("Lang-Secretary")


# 세션 상태에 대화 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 페이지 타이틀
st.title("💬")

# 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if user_prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지를 세션에 저장
    st.session_state.messages.append({"role": "user", 
                                      "content": user_prompt})
    
    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 여기에서 챗봇 응답 생성 (예시: 에코 응답)
    response = requests.post(f"{backend_url}/graphbot/invoke", 
                                 json={
                                        "input": {
                                          "input": user_prompt,
                                          "route": "string",
                                          "response": "string"
                                        },
                                        "config": {},
                                        "kwargs": {}
                                      })
    

    print(response.json())
    
    
    try:
        # 챗봇 응답을 세션에 저장
        st.session_state.messages.append({"role": "assistant", 
                                          "content": response.json()['output']['response']})
        
        # 챗봇 응답 출력
        with st.chat_message("assistant"):
            st.markdown(response.json()['output']['response'])

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", 
                                          "content": "응답에 실패하였습니다. \nException: " + str(e)})
        
        with st.chat_message("assistant"):
            st.markdown("응답에 실패하였습니다. \nException: " + str(e))
    
    
