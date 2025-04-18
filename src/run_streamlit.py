import streamlit as st
import requests


from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")


st.set_page_config(page_title="LangGraph Chat Bot", page_icon=":shark:")
st.title("LangGraph Chat Bot")


if ENV == "dev":
    backend_url = "http://localhost:8000"
else:
    backend_url = "http://lang-backend:8000"


with st.form("Question"):
    text = st.text_area("질문 입력: ")
    submitted = st.form_submit_button("보내기")
    
    if submitted:
        response = requests.post(f"{backend_url}/graphbot/invoke", 
                                 json={
                                        "input": {
                                          "input": text,
                                          "route": "string",
                                          "response": "string"
                                        },
                                        "config": {},
                                        "kwargs": {}
                                      })
        print(type(response))
        print(response.json())
        st.write(f"node state: {response.json()['output']['route']}")
        st.write(f"[response]\n{response.json()['output']['response']}")



# if __name__ == "__main__":
#     run_streamlit()
