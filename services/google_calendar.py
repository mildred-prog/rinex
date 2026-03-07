# services/google_calendar.py

import os
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
]

TIME_ZONE = "Europe/London"


class GoogleCalendarService:
    """
    Google Calendar service for Rinex Shine.

    Responsibilities:
    - authenticate with Google Calendar
    - fetch events from the selected calendar
    - calculate busy periods
    - generate real bookable slots based on service duration
    """

    def __init__(self, credentials_path=None, token_path=None, calendar_id="primary"):
        self.credentials_path = credentials_path or "credentials.json"
        self.token_path = token_path or "token.json"
        self.calendar_id = calendar_id
        self.timezone = ZoneInfo(TIME_ZONE)
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate and build the Google Calendar API client."""
        creds = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path,
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def get_calendar_list(self):
        """Return available calendars for the authenticated user."""
        try:
            result = self.service.calendarList().list().execute()
            return result.get("items", [])
        except HttpError as error:
            raise RuntimeError(f"Failed to fetch calendar list: {error}") from error

    def get_events(self, calendar_id=None, days_ahead=14):
        """
        Return upcoming events for the next N days.
        """
        calendar_id = calendar_id or self.calendar_id

        now = datetime.now(self.timezone)
        end = now + timedelta(days=days_ahead)

        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now.isoformat(),
                timeMax=end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            return events_result.get("items", [])

        except HttpError as error:
            raise RuntimeError(f"Failed to fetch events: {error}") from error

    def get_availability(self, subservice, days_ahead=14, working_hours=None, buffer_minutes=0):
        """
        Return bookable slots based on:
        - business working hours
        - existing Google Calendar events
        - selected subservice duration
        - optional buffer time

        Each returned slot has:
        - date
        - start_time
        - end_time
        - duration_minutes
        """
        if working_hours is None:
            working_hours = self._default_working_hours()

        service_duration = int(subservice.duration_minutes or 90)
        total_minutes = service_duration + int(buffer_minutes)

        events = self.get_events(days_ahead=days_ahead)
        availability = []

        today = datetime.now(self.timezone).date()

        for day_offset in range(days_ahead):
            current_date = today + timedelta(days=day_offset)
            day_name = current_date.strftime("%A").lower()
            day_hours = working_hours.get(day_name)

            if not day_hours or day_hours["start"] == "closed":
                continue

            day_start = self._combine_date_and_time(current_date, day_hours["start"])
            day_end = self._combine_date_and_time(current_date, day_hours["end"])

            busy_slots = self._get_busy_slots_for_day(events, current_date)

            slot_start = day_start
            slot_step = timedelta(minutes=30)
            slot_length = timedelta(minutes=total_minutes)

            while slot_start + slot_length <= day_end:
                slot_end = slot_start + slot_length

                if not self._overlaps_busy_slot(slot_start, slot_end, busy_slots):
                    availability.append({
                        "date": current_date,
                        "start_time": slot_start,
                        "end_time": slot_end,
                        "duration_minutes": total_minutes,
                    })

                slot_start += slot_step

        return availability

    def _default_working_hours(self):
        """Default Rinex Shine working hours."""
        return {
            "monday": {"start": "09:00", "end": "17:00"},
            "tuesday": {"start": "09:00", "end": "17:00"},
            "wednesday": {"start": "09:00", "end": "17:00"},
            "thursday": {"start": "09:00", "end": "17:00"},
            "friday": {"start": "09:00", "end": "17:00"},
            "saturday": {"start": "09:00", "end": "15:00"},
            "sunday": {"start": "closed", "end": "closed"},
        }

    def _combine_date_and_time(self, date_obj, time_string):
        """Combine a date and HH:MM string into a timezone-aware datetime."""
        hour, minute = map(int, time_string.split(":"))
        return datetime.combine(
            date_obj,
            time(hour=hour, minute=minute),
            tzinfo=self.timezone,
        )

    def _get_busy_slots_for_day(self, events, current_date):
        """
        Extract busy datetime ranges for a given date from Google events.
        Ignores all-day events for now unless you want them treated as fully busy.
        """
        busy_slots = []

        for event in events:
            start_info = event.get("start", {})
            end_info = event.get("end", {})

            if "dateTime" not in start_info or "dateTime" not in end_info:
                continue

            start_time = datetime.fromisoformat(
                start_info["dateTime"].replace("Z", "+00:00")
            ).astimezone(self.timezone)

            end_time = datetime.fromisoformat(
                end_info["dateTime"].replace("Z", "+00:00")
            ).astimezone(self.timezone)

            if start_time.date() == current_date:
                busy_slots.append((start_time, end_time))

        busy_slots.sort(key=lambda item: item[0])
        return busy_slots

    def _overlaps_busy_slot(self, slot_start, slot_end, busy_slots):
        """Return True if the proposed slot overlaps an existing busy period."""
        for busy_start, busy_end in busy_slots:
            if slot_start < busy_end and slot_end > busy_start:
                return True
        return False