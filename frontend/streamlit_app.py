import streamlit as st
import requests
import subprocess
import sys



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
        st.write(f"node state: {response.json()['output']['route']}")
        st.write(f"[response]\n{response.json()['output']['response']}")



# if __name__ == "__main__":
#     run_streamlit()
