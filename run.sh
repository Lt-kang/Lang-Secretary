#!/bin/bash

# 백엔드 (FastAPI) 실행 (백그라운드)
uvicorn src.run_api:app --host 0.0.0.0 --port 8000 &

# 프론트엔드 (Streamlit) 실행
streamlit run frontend/run_streamlit.py --server.port=8501 --server.address=0.0.0.0