from fastapi import FastAPI
import uvicorn

from langserve import add_routes
from chain import runnable_chain


# from pydantic import BaseModel
# class MyInput(BaseModel):
#     text: str


app = FastAPI()
add_routes(app, runnable_chain, path="/graphbot")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)