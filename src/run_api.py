from fastapi import FastAPI
import uvicorn

from langserve import add_routes
from src.graphs.graph_builder import build_graph




app = FastAPI()
runnable_chain = build_graph()
add_routes(app, runnable_chain, path="/graphbot")

if __name__ == "__main__":
    uvicorn.run("src.run_api:app", host="0.0.0.0", port=8000, reload=True)