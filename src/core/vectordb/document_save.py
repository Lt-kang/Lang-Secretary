from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma



def document_saver(document:Document, vector_db:Chroma):
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = splitter.split_documents([document])

        vector_db.add_documents(split_docs)
        return True
    
    except Exception as e:
        print(f"Error saving document: {e}")
        return False




