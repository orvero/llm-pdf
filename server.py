from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from dotenv import load_dotenv

load_dotenv()
loader = TextLoader("state_of_the_union.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

query = "what is the austal?"

andswer = index.query(query)
print(andswer)
