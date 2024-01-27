from langchain_community.document_loaders import YoutubeLoader

def load_youtube(url):
    # remove https://www.youtube.com/watch?v=
    url = url.split("=")[-1]
    loader = YoutubeLoader(url, language=["ko", "en"])  # 'ko'가 우선, 없을 경우 'en' 사용
    documents = loader.load()
    return documents
