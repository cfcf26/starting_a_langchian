from langchain_community.document_loaders import YoutubeLoader

from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser

import os
import shutil

def load_youtube_audio(url):
    urls = [url]
    save_dir = "~/data/youtube_audio"
    loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
    documents = loader.load()
     # 생성된 음성 파일 삭제
    shutil.rmtree(os.path.expanduser(save_dir))
    return documents

def load_youtube(url):
    # remove https://www.youtube.com/watch?v=
    urls = url.split("=")[-1]
    loader = YoutubeLoader(urls, language=["ko", "en"])  # 'ko'가 우선, 없을 경우 'en' 사용
    documents = loader.load()
    if len(documents) == 0:
        documents = load_youtube_audio(url)
    if len(documents) == 0:
        raise Exception("No documents found")
    return documents
