from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json

class Command(BaseCommand):
    help = 'Setup Google Calendar credentials for availability integration'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--setup',
            action='store_true',
            help='Create credentials.json template',
        )
    
    def handle(self, *args, **options):
        if options['setup']:
            self.setup_credentials()
        else:
            self.show_instructions()
    
    def setup_credentials(self):
        """Create a credentials.json template file"""
        credentials_template = {
            "web": {
                "client_id": "YOUR_CLIENT_ID_HERE",
                "project_id": "YOUR_PROJECT_ID_HERE", 
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET_HERE",
                "redirect_uris": ["http://localhost:8080/"]
            }
        }
        
        credentials_path = 'credentials.json'
        
        if os.path.exists(credentials_path):
            self.stdout.write(
                self.style.WARNING(f'Credentials file {credentials_path} already exists!')
            )
            return
        
        with open(credentials_path, 'w') as f:
            json.dump(credentials_template, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {credentials_path} template')
        )
        self.show_next_steps()
    
    def show_instructions(self):
        """Show setup instructions"""
        instructions = """
🗓️  GOOGLE CALENDAR SETUP INSTRUCTIONS

1. CREATE GOOGLE CLOUD PROJECT:
   - Go to: https://console.cloud.google.com/
   - Create new project or select existing one

2. ENABLE CALENDAR API:
   - Go to: https://console.cloud.google.com/apis/library/calendar.googleapis.com
   - Enable the Google Calendar API

3. CREATE CREDENTIALS:
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Web application"
   - Add redirect URI: http://localhost:8080/
   - Download JSON file and save as 'credentials.json'

4. RUN SETUP COMMAND:
   python manage.py setup_calendar --setup

5. TEST AUTHENTICATION:
   - Run: python manage.py test_calendar_auth
   - This will open browser for OAuth authentication

6. CONFIGURE CALENDAR:
   - Share your Google Calendar with the service account
   - Set up working hours in Django settings

📋 NEXT STEPS:
- Run the setup command to create credentials template
- Follow the Google Cloud Console steps above
- Test the authentication
- Configure your calendar availability
        """
        
        self.stdout.write(self.style.SUCCESS(instructions))
    
    def show_next_steps(self):
        """Show what to do after creating credentials template"""
        next_steps = """
📝 NEXT STEPS:

1. EDIT credentials.json:
   Replace placeholder values with your actual Google Cloud credentials:
   - YOUR_CLIENT_ID_HERE
   - YOUR_PROJECT_ID_HERE  
   - YOUR_CLIENT_SECRET_HERE

2. TEST AUTHENTICATION:
   python manage.py test_calendar_auth

3. CONFIGURE IN SETTINGS:
   Add to settings.py:
   GOOGLE_CALENDAR_ID = 'primary'  # or your calendar ID
   CALENDAR_WORKING_HOURS = {
       'monday': {'start': '09:00', 'end': '17:00'},
       'tuesday': {'start': '09:00', 'end': '17:00'},
       'wednesday': {'start': '09:00', 'end': '17:00'},
       'thursday': {'start': '09:00', 'end': '17:00'},
       'friday': {'start': '09:00', 'end': '17:00'},
       'saturday': {'start': '09:00', 'end': '15:00'},
       'sunday': {'start': 'closed', 'end': 'closed'},
   }
        """
        
        self.stdout.write(self.style.SUCCESS(next_steps))
