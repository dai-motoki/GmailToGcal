
import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Load credentials from file
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# Build the Gmail service
service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API to fetch the latest emails
results = service.users().messages().list(userId='me', maxResults=10).execute()
messages = results.get('messages', [])

if not messages:
    print('No messages found.')
else:
    print('Message snippets:')
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print(msg['snippet'])

