from web_loader import load_web, load_web_v2
from summarize_documents import summarize
from save_to_notion import save_to_notion
from langchain_openai import ChatOpenAI

import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

# import requests
# from bs4 import BeautifulSoup

# def load_web(url):
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     return soup

if __name__ == '__main__':
    url = 'https://chat.openai.com/share/f98eec3f-57bd-451b-9b50-e34db93a4bb5'
    documents = load_web([url]) 
    print("정적 웹 : ")
    print(documents)
    documents2 = load_web_v2([url]) 
    print("동적 웹 : ")
    print(documents2)