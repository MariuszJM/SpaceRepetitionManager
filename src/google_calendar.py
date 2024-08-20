from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
from datetime import datetime, timezone


class GoogleCalendar:
    """
    Manages interactions with the Google Calendar API, including authentication, and creating, updating, and deleting events.
    """

    def __init__(self, calendar_id, credentials_file):
        """
        Initializes the GoogleCalendar instance with credentials and sets up the Google Calendar service.

        :param calendar_id: The ID of the Google Calendar to manage.
        :param credentials_file: Path to the OAuth 2.0 client secrets file.
        """
        self.calendar_id = calendar_id
        self.credentials = None
        self.service = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if (
                self.credentials
                and self.credentials.expired
                and self.credentials.refresh_token
            ):
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    scopes=["https://www.googleapis.com/auth/calendar"],
                )
                self.credentials = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(self.credentials, token)

        self.service = build("calendar", "v3", credentials=self.credentials)

    def create_event(self, summary, description, start_time, end_time):
        """
        Creates a new event in the Google Calendar.

        :param summary: The summary or title of the event.
        :param description: The description of the event.
        :param start_time: The start time of the event in RFC3339 format.
        :param end_time: The end time of the event in RFC3339 format.
        :return: The created event object.
        """
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "Europe/Warsaw"},
            "end": {"dateTime": end_time, "timeZone": "Europe/Warsaw"},
            "colorId": "8",
        }

        created_event = (
            self.service.events()
            .insert(calendarId=self.calendar_id, body=event)
            .execute()
        )
        return created_event

    def update_event(self, event_id, update_body):
        """
        Updates an existing event in the Google Calendar.

        :param event_id: The ID of the event to update.
        :param update_body: A dictionary containing the event attributes to update.
        :return: The updated event object.
        """
        updated_event = (
            self.service.events()
            .update(calendarId=self.calendar_id, eventId=event_id, body=update_body)
            .execute()
        )
        return updated_event

    def delete_event(self, event_id):
        """
        Deletes an event from the Google Calendar.

        :param event_id: The ID of the event to delete.
        """
        self.service.events().delete(
            calendarId=self.calendar_id, eventId=event_id
        ).execute()

    def get_events(self, start_date, end_date):
        """
        Retrieves events from the Google Calendar within a specified date range.

        :param start_date: The start date for the events query in YYYY-MM-DD format.
        :param end_date: The end date for the events query in YYYY-MM-DD format.
        :return: A list of event objects within the specified date range.
        """
        start_datetime = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        end_datetime = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
        start_date_str = start_datetime.isoformat()
        end_date_str = end_datetime.isoformat()

        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=start_date_str,
                    timeMax=end_date_str,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return events_result.get("items", [])
        except Exception as e:
            print("An error occurred while fetching events:", e)
            return []
