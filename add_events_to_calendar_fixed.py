
import datetime
import pickle
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

# Load credentials from file
with open('credentials.json', 'r') as file:
    credentials_data = json.load(file)

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_config(credentials_data, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

# Function to add an event to the calendar
def add_event_to_calendar(event):
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

# Read the tasks.json file
with open('tasks.json', 'r') as file:
    tasks_data = json.load(file)

# Extract the event details and correct the dateTime format
events = []
for task in tasks_data['tasks']:
    start_time, end_time = task['期限'].split('~')
    event = {
        'summary': task['内容'],
        'start': {'dateTime': start_time.replace('/', '-') + ':00', 'timeZone': 'Asia/Tokyo'},
        'end': {'dateTime': end_time.replace('/', '-') + ':00', 'timeZone': 'Asia/Tokyo'}
    }
    event['start']['dateTime'] = event['start']['dateTime'].replace(' ', 'T')
    end_date = start_time.split(' ')[0]  # Get the date from the start time
    if '00:00' in end_time:  # Check if the end time indicates the next day
        end_date_time = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date_time.strftime('%Y-%m-%d')
    event['end']['dateTime'] = end_date + 'T' + end_time.split('~')[1]
    events.append(event)

# Add each event to the calendar
for event in events:
    try:
        event_link = add_event_to_calendar(event)
        print(f"Event added: {event['summary']} Link: {event_link}")
    except Exception as e:
        print(f"An error occurred: {e}")
