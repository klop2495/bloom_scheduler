from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'my-studio-1509831528967-102d93b1bb20.json'  # 👈 имя твоего JSON-файла

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def add_event_to_calendar(event_data, calendar_id='primary'):
    service = get_calendar_service()
    event = {
        'summary': event_data['title'],
        'start': {'dateTime': event_data['start'], 'timeZone': 'Europe/Paris'},
        'end': {'dateTime': event_data['end'], 'timeZone': 'Europe/Paris'},
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()

def get_upcoming_events(calendar_id='primary', max_results=10):
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

