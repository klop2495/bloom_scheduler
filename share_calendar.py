from google.oauth2 import service_account
from googleapiclient.discovery import build
import os, base64, tempfile

GOOGLE_CREDENTIALS_B64 = os.environ.get("GOOGLE_CREDENTIALS_B64")
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds_data = base64.b64decode(GOOGLE_CREDENTIALS_B64)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(creds_data)
        temp_file.flush()
        credentials = service_account.Credentials.from_service_account_file(
            temp_file.name, scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)

def create_calendar():
    service = get_calendar_service()
    calendar = {'summary': 'Bloom — Расписание съёмок', 'timeZone': 'Europe/Paris'}
    created = service.calendars().insert(body=calendar).execute()
    print("✅ Календарь создан:", created['id'])
    return created['id']

def share_calendar_with_user(calendar_id, user_email):
    service = get_calendar_service()
    rule = {'scope': {'type': 'user', 'value': user_email}, 'role': 'writer'}
    created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
    print(f"✅ Расшарено с {user_email}: {created_rule['id']}")

# === ЗАПУСК ===
calendar_id = create_calendar()
share_calendar_with_user(calendar_id, "epsilonpix@gmail.com")

