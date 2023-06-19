from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from dotenv import load_dotenv
from os import path

load_dotenv()


def query_Pdf(question, fileName):
    loader = PyPDFLoader(path.join("queryfiles", fileName))
    index = VectorstoreIndexCreator().from_loaders([loader])
    query = question
    answer = index.query(query)
    return answer
