from notion_client import Client

import re
import datetime
import os
import dotenv
dotenv.load_dotenv(verbose=True)

def extract_title(summary):
    # 정규 표현식을 사용하여 제목 추출
    match = re.search(r'제목: (.+?)\n', summary)
    return match.group(1) if match else 'No Title Found'

def save_to_notion(url, summaries, type):
    notion_api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    notion = Client(auth=notion_api_key)
    
    title = extract_title(summaries.get('output_text', ''))

    # Create a new page
    new_page = notion.pages.create(parent={"database_id": database_id}, properties={
        "title": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Type": {
            "select": {
                "name": type
            }
        },
        "Created": {
            "date": {
                "start": current_datetime
            }
        },
        "URL": {
            "url": url
        }
    })

    # Add summary to the page
    notion.blocks.children.append(block_id=new_page["id"], children=[
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": summaries.get('output_text', '')
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "embed",
            "embed": {
                "url": url
            }
        }
    ])