import streamlit as st
import requests


st.set_page_config(page_title="LangGraph Chat Bot", page_icon=":shark:")
st.title("LangGraph Chat Bot")


with st.form("Question"):
    text = st.text_area("질문 입력: ")
    submitted = st.form_submit_button("보내기")
    
    if submitted:
        response = requests.post("http://localhost:8000/graphbot/invoke", json={
  "input": {
    "input": text,
    "route": "string",
    "response": "string"
  },
  "config": {},
  "kwargs": {}
})
        print(response.json())
        st.write(f"LangGraph-bot node state: {response.json()['output']['route']}")
        st.write(f"LangGraph-bot response: {response.json()['output']['response']}")