import os.path
import re

import datetime
from datetime import datetime
from dateutil import parser, tz
from typing import List, Optional, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def check_auth():
    """Authenticate Google Calendar API"""
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

def standardize_datetime(date_str: str):
    # Check if string is already in ISO 8601 format
    iso_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d+)?(Z|[+-]\d{2}:\d{2})$')
    if iso_pattern.match(date_str):
        return date_str
    
    else:
        parsed_date = parser.parse(date_str).replace(microsecond=0)

        # Check if timezone is already included
        if parsed_date.tzinfo is not None:
            return parsed_date.isoformat()

        # Assume date provided is in localtime
        else:
            local_tz = tz.tzlocal()
            date_local = parsed_date.replace(tzinfo=local_tz)    
            return date_local.isoformat()

def read_event(
    start_time: str,
    end_time: str,
    top_n: int = 10
):
    """Get events from Google Calendar"""
   
    creds = check_auth()
    try:
        service = build("calendar", "v3", credentials=creds)
        
        print(f"Fetching calendar events from {start_time} to {end_time}")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                timeMax=end_time,
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

def create_event(event: dict):
    """Add event to Google Calendar"""
    
    creds = check_auth()
    
    try:
        service = build("calendar", "v3", credentials=creds)
        
        # update calendar with event
        event = service.events().insert(calendarId='primary', body=event).execute()
        
        print("Event Added")
        return event.get('htmlLink')

    except Exception as e:
        print(f"Error in creating the event: {e}")

def update_event(event: dict):
    """Update event in Google Calendar"""
    
    creds = check_auth()

    try:
        service = build("calendar", "v3", credentials=creds)
        
        # update calendar with event
        updated_event = service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()
        
        print("Event Updated")
        return updated_event.get("htmlLink")

    except Exception as e:
        print(f"Error in updating the event: {e}")

def delete_event(event: dict):
    """Delete event from Google Calendar"""

    creds = check_auth()
    
    try:
        service = build("calendar", "v3", credentials=creds)
        
        # delete calendar with event
        service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        
        print("Event Deleted", event["summary"])

    except Exception as e:
        print(f"Error in deleting the event: {e}")



if __name__ == "__main__":
    # Read events from Google Calendar
    events = read_event(
        time_start="2025-04-13T00:00:00+08:00",
        time_end="2025-04-20T00:00:00+08:00",
        top_n=10
    )

    for event in events:
        if event["eventType"] == "default":
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])


