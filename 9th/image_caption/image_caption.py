from langchain_community.document_loaders import ImageCaptionLoader

import requests
import datetime

def download_image(image_url):
    # URL에서 파일 이름 추출
    file_name = f"image{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

    # 이미지 다운로드 및 저장
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully: {file_name}")
    else:
        raise Exception(f"Error: Unable to download image. Status code: {response.status_code}")

def load_image_caption(image_url):
    loader = ImageCaptionLoader(image_url)
    documents = loader.load()
    return documents