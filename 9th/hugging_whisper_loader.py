from huggingface_models import huggingface_whisper_large_v3_from_url
from summarize_documents import summarize
from langchain_openai import ChatOpenAI

import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

if __name__ == '__main__':
    url = "https://youtu.be/KdbPZNdFJU0?si=dZFI7pr_iGHG03Ji"
    save_dir = "path/to/save/directory"
    documents = huggingface_whisper_large_v3_from_url(url, save_dir)
    summaries = summarize(llm, documents)