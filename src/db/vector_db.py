from pathlib import Path


from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from src.config import VECTOR_DB_PATH


embedding = OpenAIEmbeddings()


def init_vector_db(persist_directory:str = VECTOR_DB_PATH):
    if Path(persist_directory).exists():
        print("Load Vector DB from ", persist_directory)
    else:
        print("Init Vector DB")

    return Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory
    )


if __name__ == "__main__":
    vector_db = init_vector_db()
    print(vector_db)
