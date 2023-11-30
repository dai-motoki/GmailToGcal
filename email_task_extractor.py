import base64
import requests
import csv

# OpenAI API Key
api_key = "your_api_key"

# ヘッダーの設定
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

# メールからテキストを取得
with open('latest_email.txt', 'r') as email_file:
    email_text = email_file.read()

# ペイロードの設定

from datetime import date

from datetime import datetime
今日の日付 = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


prompt = 今日の日付 + "（今日の日時）を基準にして"+ email_text + """
          からタスクを以下の形でjson形式で抽出して。
          例：
            {
                "tasks": [
                    {
                        "期限": "2021/10/31 13:00~14:00",（必ず設定する。ゆとりを持って設定する。開始から終了時刻まで記載）
                        "内容": "メールからタスクを抽出する"
                    }
                ]
            }
          """


payload = {
  "model": "gpt-4-1106-preview",
  "response_format": { "type": "json_object" },
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt
        },
      ]
    }
  ],
  "max_tokens": 300
}

# OpenAI APIにリクエストを送信
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# レスポンスをJSON形式で取得し、タスクを抽出
response_json = response.json()

content = response_json['choices'][0]['message']['content']

print(content)

import json

# タスクをjsonファイルに保存
with open('tasks.json', 'w', encoding='utf-8') as json_file:
    json.dump(json.loads(content), json_file, ensure_ascii=False)
