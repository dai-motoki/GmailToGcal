
import base64
import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email import message_from_bytes

# Load credentials from file
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# Build the Gmail service
service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API to fetch the latest email
results = service.users().messages().list(userId='me', maxResults=1).execute()
messages = results.get('messages', [])

if not messages:
    print('メッセージが見つかりませんでした。')
else:
    message = messages[0]  # 最新のメッセージを取得
    msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    msg_bytes = base64.urlsafe_b64decode(msg['raw'])
    mime_msg = message_from_bytes(msg_bytes)

    # MIMEメッセージからコンテンツを抽出する関数
    def get_mime_message_payload(mime_message):
        if mime_message.is_multipart():
            for part in mime_message.get_payload():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode('utf-8')
        else:
            return mime_message.get_payload(decode=True).decode('utf-8')

    email_content = get_mime_message_payload(mime_msg)

    # HTMLタグを削除
    import re
    email_content = re.sub('<[^<]+?>', '', email_content)

    # メールの内容をテキストファイルに保存
    with open('latest_email.txt', 'w') as email_file:
        email_file.write(email_content)

    print('最新のメールの内容がlatest_email.txtに保存されました。')
