from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.documents.base import Document

import os
os.getenv('OPENAI_API_KEY')

import requests
import datetime
import base64

def download_image(image_url):
    # URL에서 파일 이름 추출
    file_name = f"image{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

    # 이미지 다운로드 및 저장
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully: {file_name}")
        return file_name
    else:
        raise Exception(f"Error: Unable to download image. Status code: {response.status_code}")


def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def load_image_caption(url):
    """Make image summary"""
    file_name = download_image(url)
    
    base64_string = encode_image(file_name)
    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)

    try:
        chat_completion = chat.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": "Describe the image:"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpg;base64,{base64_string}"},
                        },
                    ]
                )
            ]
        )

        # Inspect the chat_completion object
        print("Response object:", type(chat_completion.content))
        
        # Create a Document object with the image description
        document = Document(page_content=chat_completion.content)

        return [document]
    except Exception as e:
        print("An error occurred:", e)
        return []
