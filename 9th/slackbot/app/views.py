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

processed_events = set()

@csrf_exempt
@require_POST
def slack_events(request):
    json_data = json.loads(request.body)

    if 'challenge' in json_data:
        return JsonResponse({'challenge': json_data['challenge']})
    event_id = json_data['event_id']
    # 이미 처리된 event_id인지 확인
    if event_id in processed_events:
        return JsonResponse({'status': 'OK'})  # 중복 요청 처리
    if json_data['event']['type'] == 'message' and json_data['event']['channel_type'] == 'im':
        text = json_data['event']['text']

        # ChatOpenAI 인스턴스 생성
        key = os.getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(api_key=key, temperature=0)
        # URLAgent 인스턴스 생성
        JsonResponse({'status': 'OK'})
        URLAgent(llm, text)
        
        # 처리된 event_id 저장
        processed_events.add(event_id)
    return JsonResponse({'status': 'OK'})
