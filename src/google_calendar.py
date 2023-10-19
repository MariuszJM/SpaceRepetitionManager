from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request  # Dodane
import os
import pickle
from datetime import datetime, timezone

class GoogleCalendar:
    def __init__(self, calendar_id, credentials_file):
        self.calendar_id = calendar_id
        self.credentials = None
        self.service = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())  # Poprawione
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
                self.credentials = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

        self.service = build('calendar', 'v3', credentials=self.credentials)

    def create_event(self, summary, description, start_time, end_time):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Warsaw',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Warsaw',
            }
        }

        created_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return created_event

    def update_event(self, event_id, update_body):
        updated_event = self.service.events().update(
            calendarId=self.calendar_id,
            eventId=event_id,
            body=update_body
        ).execute()
        return updated_event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def get_events(self, start_date, end_date):
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
        start_datetime = start_datetime.replace(tzinfo=timezone.utc)
        end_datetime = end_datetime.replace(tzinfo=timezone.utc)
        start_date_str = start_datetime.isoformat()
        end_date_str = end_datetime.isoformat()

        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_date_str,
                timeMax=end_date_str,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            print("Wystąpił błąd podczas próby pobrania wydarzeń:", e)
            return []
