import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarService:
    def __init__(self, credentials_path=None):
        self.credentials_path = credentials_path or 'credentials.json'
        self.token_path = 'token.json'
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Handles Google Calendar authentication"""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def get_calendar_list(self):
        """Get list of user's calendars"""
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list.get('items', [])
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def get_events(self, calendar_id='primary', days_ahead=30):
        """Get events from calendar for the next N days"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=calendar_id, 
                timeMin=now, 
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def get_availability(self, calendar_id='primary', days_ahead=30, working_hours=None):
        """
        Get availability slots based on existing events
        Returns available time slots for booking
        """
        if working_hours is None:
            working_hours = {
                'monday': {'start': '09:00', 'end': '17:00'},
                'tuesday': {'start': '09:00', 'end': '17:00'},
                'wednesday': {'start': '09:00', 'end': '17:00'},
                'thursday': {'start': '09:00', 'end': '17:00'},
                'friday': {'start': '09:00', 'end': '17:00'},
                'saturday': {'start': '09:00', 'end': '15:00'},
                'sunday': {'start': 'closed', 'end': 'closed'}
            }
        
        events = self.get_events(calendar_id, days_ahead)
        availability = []
        
        # Process each day to find available slots
        for day_offset in range(days_ahead):
            current_date = datetime.utcnow() + timedelta(days=day_offset)
            day_name = current_date.strftime('%A').lower()
            
            if working_hours.get(day_name, {}).get('start') == 'closed':
                continue
            
            # Create busy slots from events
            busy_slots = []
            for event in events:
                start_str = event['start'].get('dateTime', event['start'].get('date'))
                end_str = event['end'].get('dateTime', event['end'].get('date'))
                
                if 'dateTime' in event['start']:  # Time-specific event
                    start_time = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    
                    # Only consider events on the current day
                    if start_time.date() == current_date.date():
                        busy_slots.append((start_time, end_time))
            
            # Generate available slots
            day_start = current_date.replace(
                hour=int(working_hours[day_name]['start'].split(':')[0]),
                minute=int(working_hours[day_name]['start'].split(':')[1]),
                second=0, microsecond=0
            )
            
            day_end = current_date.replace(
                hour=int(working_hours[day_name]['end'].split(':')[0]),
                minute=int(working_hours[day_name]['end'].split(':')[1]),
                second=0, microsecond=0
            )
            
            # Find gaps between busy slots
            available_slots = self._find_available_slots(day_start, day_end, busy_slots)
            
            for slot_start, slot_end in available_slots:
                availability.append({
                    'date': current_date.date(),
                    'start_time': slot_start,
                    'end_time': slot_end,
                    'duration_minutes': int((slot_end - slot_start).total_seconds() / 60)
                })
        
        return availability
    
    def _find_available_slots(self, day_start, day_end, busy_slots, min_slot_minutes=30):
        """Find available time slots between busy periods"""
        if not busy_slots:
            return [(day_start, day_end)]
        
        # Sort busy slots by start time
        busy_slots.sort(key=lambda x: x[0])
        
        available_slots = []
        current_time = day_start
        
        for busy_start, busy_end in busy_slots:
            # If there's a gap before this busy slot
            if current_time < busy_start:
                gap_duration = (busy_start - current_time).total_seconds() / 60
                if gap_duration >= min_slot_minutes:
                    available_slots.append((current_time, busy_start))
            
            # Move current time to after this busy slot
            current_time = max(current_time, busy_end)
        
        # Check if there's time after the last busy slot
        if current_time < day_end:
            gap_duration = (day_end - current_time).total_seconds() / 60
            if gap_duration >= min_slot_minutes:
                available_slots.append((current_time, day_end))
        
        return available_slots
