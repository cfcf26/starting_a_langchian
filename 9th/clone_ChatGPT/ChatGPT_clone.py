from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import dotenv
import os


dotenv.load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(api_key=key, temperature=0)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

query_text = "FAISS"
query_text2 = "FAISS is a vector store."
query_text3 = "LangChain"
query_text4 = "LangChain is a library."


embed_query = embeddings.embed_query(query_text)
embed_query2 = embeddings.embed_query(query_text2)
embed_query3 = embeddings.embed_query(query_text3)
embed_query4 = embeddings.embed_query(query_text4)
print(embed_query[:5])
print(embed_query2[:5])
print(embed_query3[:5])
print(embed_query4[:5])

input = "FAISS is a vector store."

texts = ["FAISS is an important library", "LangChain supports FAISS"]
faiss_instance = FAISS.from_texts(texts, embeddings)
similar_docs = faiss_instance.similarity_search(input, k=1)
print(similar_docs)