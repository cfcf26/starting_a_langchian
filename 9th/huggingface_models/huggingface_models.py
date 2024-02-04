from langchain_core.documents.base import Document
import requests
import os
import yt_dlp
import time
import os
import dotenv
dotenv.load_dotenv(verbose=True)

key = os.getenv('HUGGINGFACE_API_KEY')

from pydub import AudioSegment

def split_m4a(file_path, segment_length=30000):
    # 파일의 확장자를 제외한 이름을 가져옵니다.
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # 오디오 파일을 불러옵니다.
    audio = AudioSegment.from_file(file_path, format="m4a")

    # 오디오 파일을 주어진 길이(기본 30초)로 나눕니다.
    parts = len(audio) // segment_length

    # 분할된 파일들의 이름을 저장할 리스트
    file_names = []

    for i in range(parts):
        # 오디오 분할
        start = i * segment_length
        end = start + segment_length
        split_audio = audio[start:end]

        # 분할된 오디오 파일 저장
        split_filename = f"{base_name}_part{i}.mp3"
        split_audio.export(split_filename, format="mp3")
        file_names.append(split_filename)

    return file_names

# 예시 사용법
# file_names = split_m4a("your_file.m4a")
# print(file_names)


def download_youtube_audio(url, save_dir):
    """Download audio file from a YouTube URL."""
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "noplaylist": True,
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Assuming only one file is downloaded, return its path
    downloaded_files = [f for f in os.listdir(save_dir) if f.endswith('.m4a')]
    print("downloaded_files: ", downloaded_files)
    return os.path.join(save_dir, downloaded_files[0]) if downloaded_files else None


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {f"Authorization": "Bearer {key}"}

def query(filename):
    attempts = 0
    while attempts < 5:
        try:
            with open(filename, 'rb') as file_obj:
                response = requests.post(API_URL, headers=headers, files={'file': file_obj})
            response_json = response.json()

            # 서버에서 반환된 오류 처리
            if 'error' in response_json:
                print(f"Error in response: {response_json['error']}")
                if 'Model openai/whisper-large-v3 is currently loading' in response_json.get('error', ''):
                    wait_time = response_json.get('estimated_time', 10)
                    print(f"Waiting for model to load: {wait_time} seconds")
                    time.sleep(wait_time)
                    attempts += 1
                    continue
                else:
                    break

            return response_json  # 성공적인 응답 반환
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            attempts += 1
            time.sleep(5)  # 재시도 전 5초 대기

    print("Failed to get response after several attempts")
    return None


def huggingface_whisper_large_v3(filename):
    print("filename : " + filename)
    results = []
    print("Transcribing audio file!")
    try:
        response_json = query(filename)  # .json() 호출 제거
        print("response_json " + str(response_json))
        if 'error' in response_json:
            print(f"Error in response: {response_json['error']}")
            return results

        transcript = response_json['text']
        print(transcript)
        results.append(Document(
            page_content=transcript,
            metadata={"source": filename}
        ))
    except Exception as e:
        print(f"Failed to transcribe audio file. Exception: {str(e)}")

    return results




def huggingface_whisper_large_v3_from_url(url, save_dir):
    print(url, save_dir)
    """Process a YouTube URL with Whisper API."""
    audio_file_path = download_youtube_audio(url, save_dir)
    files = split_m4a(audio_file_path)
    print("files: ", files)
    documents = []
    for file in files:
        documents += huggingface_whisper_large_v3(file)
        
    # Remove the downloaded files
    for file in files:
        os.remove(file)
    os.remove(audio_file_path)
    
    return documents