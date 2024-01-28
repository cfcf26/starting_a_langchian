# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from slack_sdk import WebClient
import os
from langchain_openai import ChatOpenAI

import sys
sys.path.append('../')
from url_agent import URLAgent

slack_token = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)

# 전역 변수로 처리된 이벤트 ID 저장
processed_events = set()


@csrf_exempt
@require_POST
def slack_events(request):
    json_data = json.loads(request.body)
    print(json_data)

    # 'challenge' 요청 처리
    if 'challenge' in json_data:
        return JsonResponse({'challenge': json_data['challenge']})
    
    event_id = json_data.get('event_id', '')
    # 중복된 이벤트인지 확인
    if event_id in processed_events:
        return JsonResponse({'status': 'Already processed'})

    processed_events.add(event_id)
    
    text = json_data.get('event', {}).get('text', '')

    # ChatOpenAI 인스턴스 생성 및 URLAgent 처리
    key = os.getenv('OPENAI_API_KEY')
    llm = ChatOpenAI(api_key=key, temperature=0)
    URLAgent(llm, text)

    return JsonResponse({'status': 'OK'})
