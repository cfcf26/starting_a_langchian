from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import SeleniumURLLoader

# 동적 웹
def load_web_v2(url):
    loader = SeleniumURLLoader([url], executable_path="/home/ekwak/starting_a_langchian/9th/web_loader/geckodriver", browser="firefox")
    documents = loader.load()
    return documents

# 정적 웹
def load_web_v1(url):
    loader = WebBaseLoader(url, autoset_encoding=True)
    documents = loader.load()
    return documents
