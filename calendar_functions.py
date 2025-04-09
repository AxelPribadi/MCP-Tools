import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def check_auth():
    creds=None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_events(
    top_n: int = 25,
    time_start: str = None,
    time_end: str = None,
):
    """Time Start and Time End should be in ISO format"""
    creds = check_auth()
    
    try:
        service = build("calendar", "v3", credentials=creds)
        if not time_start:
            time_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if not time_end:
            time_end = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).isoformat()
        
        print(f"Fetching calendar events from {time_start} to {time_end}")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_start,
                timeMax=time_end,
                maxResults=top_n,
                singleEvents=True,
                orderBy="startTime"
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    except Exception as e:
        print(f"Error fetching calendar events: {e}")
        return []
    
if __name__ == "__main__":
    events = get_events(10)
    for event in events:
        print(event)
