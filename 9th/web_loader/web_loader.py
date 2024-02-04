from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import SeleniumURLLoader

# 동적 웹
def load_web_v2(url):
    loader = SeleniumURLLoader(url, executable_path="/Users/kwak/starting_a_langchain/9th/web_loader/chromedriver")
    documents = loader.load()
    return documents

# 정적 웹
def load_web(url):
    loader = WebBaseLoader(url, autoset_encoding=True)
    documents = loader.load()
    return documents
