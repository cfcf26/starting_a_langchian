# 기본 환경 설정
from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(api_key=key, temperature=0)

# 1단계. KoNLPY를 이용한 텍스트 분리
from langchain.text_splitter import KonlpyTextSplitter

with open("대한민국 헌법.txt") as f:
    korean_document = f.read()

text_splitter = KonlpyTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_text(korean_document)

# 2단계 OpenAIEmbeddings를 이용한 텍스트 임베딩 생성 및 Local에 저장
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(texts, embeddings)
db.save_local("faiss_db")

# 3단계 local에 저장된 FAISS를 불러와서 새로운 문장에 대한 유사도 검색
new_db = FAISS.load_local("faiss_db", embeddings)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

retriever = new_db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.8}) # 0.8 이상의 유사도를 가진 문장을 검색

template = """Answer the question based only on the following context, which can include text and tables:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 인터페이스 만들기
import streamlit as st
# 앱 제목 설정
st.title('대한민국 헌법 검색기')
# 사용자 입력 받기
user_input = st.text_input('내용을 입력하세요:', '')
result = chain.invoke(user_input)
# 입력 받은 내용 출력
if user_input:
    st.write('입력한 내용:', result)