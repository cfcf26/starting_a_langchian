from web_loader import load_web
from summarize_documents import summarize
from langchain_openai import ChatOpenAI

import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

def save_file(url, summaries):
    with open(f'text.txt', 'w') as f:
        f.write(f'URL: {url}\n\n')
        f.write('\nSummaries:\n')
        summary_text = summaries.get('output_text', '')
        f.write(f'{summary_text}\n')

if __name__ == '__main__':
    url = input('url: ')
    documents = load_web(url)
    summaries = summarize(llm, documents)
    save_file(url, summaries)