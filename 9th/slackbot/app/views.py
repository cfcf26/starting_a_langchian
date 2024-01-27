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
    if 'challenge' in json_data:
        return JsonResponse({'challenge': json_data['challenge']})
    
    if json_data['event']['type'] == 'message' and 'subtype' not in json_data['event']:
        text = json_data['event']['text']

        # ChatOpenAI 인스턴스 생성
        key = os.getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(api_key=key, temperature=0)

        # URLAgent 인스턴스 생성
        URLAgent(llm, text)

        # 추가적인 처리...

    return JsonResponse({'status': 'OK'})
