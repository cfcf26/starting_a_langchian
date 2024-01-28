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

@csrf_exempt
@require_POST
def slack_events(request):
    json_data = json.loads(request.body)
    print(json_data)

    # 'challenge' 요청 처리
    if 'challenge' in json_data:
        return JsonResponse({'challenge': json_data['challenge']})

    # 'event' 객체와 'event_id' 확인
    if 'event' in json_data and 'event_id' in json_data:
        event = json_data['event']

        # 'text' 필드가 있는 메시지 이벤트인 경우 처리
        if event.get('type') == 'message' and event.get('channel_type') == 'im' and 'text' in event:
            text = event['text']

            # ChatOpenAI 인스턴스 생성 및 URLAgent 처리
            key = os.getenv('OPENAI_API_KEY')
            llm = ChatOpenAI(api_key=key, temperature=0)
            URLAgent(llm, text)

    return JsonResponse({'status': 'OK'})
