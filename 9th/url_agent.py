from url_agent import URLAgent
from langchain_openai import ChatOpenAI

import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=key, temperature=0)

URLAgent(llm, input('url: '))