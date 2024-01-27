from langchain_community.document_loaders import WebBaseLoader

def load_web(url):
    loader = WebBaseLoader(url, autoset_encoding=True)
    documents = loader.load()
    return documents