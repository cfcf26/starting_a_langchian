from web_loader import load_web
from summarize_documents import summarize
from save_to_notion import save_to_notion
from langchain_openai import ChatOpenAI

import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

if __name__ == '__main__':
    url = 'https://python.langchain.com/docs/integrations/document_loaders/image_captions'
    documents = load_web(url)
    summaries = summarize(llm, documents)
    save_to_notion(url, summaries, 'Web')