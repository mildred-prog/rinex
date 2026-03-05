from django.core.management.base import BaseCommand
from services.google_calendar import GoogleCalendarService
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Test Google Calendar authentication and fetch availability'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days ahead to check availability (default: 7)',
        )
    
    def handle(self, *args, **options):
        try:
            self.stdout.write('🔐 Testing Google Calendar authentication...')
            
            # Initialize calendar service
            calendar_service = GoogleCalendarService()
            self.stdout.write(self.style.SUCCESS('✅ Authentication successful!'))
            
            # Get calendar list
            calendars = calendar_service.get_calendar_list()
            self.stdout.write(f'\n📅 Found {len(calendars)} calendars:')
            for calendar in calendars[:3]:  # Show first 3 calendars
                name = calendar.get('summary', 'No name')
                calendar_id = calendar.get('id', 'No ID')
                self.stdout.write(f'  - {name} ({calendar_id})')
            
            # Get availability
            days_ahead = options['days']
            self.stdout.write(f'\n🕐 Checking availability for next {days_ahead} days...')
            
            availability = calendar_service.get_availability(days_ahead=days_ahead)
            
            if availability:
                self.stdout.write(self.style.SUCCESS(f'\n✅ Found {len(availability)} available slots:'))
                
                # Group by date
                slots_by_date = {}
                for slot in availability:
                    date_str = slot['date'].strftime('%Y-%m-%d')
                    if date_str not in slots_by_date:
                        slots_by_date[date_str] = []
                    slots_by_date[date_str].append(slot)
                
                # Show first 5 days
                for i, (date_str, slots) in enumerate(list(slots_by_date.items())[:5]):
                    self.stdout.write(f'\n📅 {date_str} ({len(slots)} slots):')
                    for slot in slots[:3]:  # Show first 3 slots per day
                        start_time = slot['start_time'].strftime('%H:%M')
                        end_time = slot['end_time'].strftime('%H:%M')
                        duration = slot['duration_minutes']
                        self.stdout.write(f'  ⏰ {start_time} - {end_time} ({duration}min)')
                    
                    if len(slots) > 3:
                        self.stdout.write(f'  ... and {len(slots) - 3} more slots')
                
                if len(slots_by_date) > 5:
                    self.stdout.write(f'\n... and {len(slots_by_date) - 5} more days')
            else:
                self.stdout.write(self.style.WARNING('\n⚠️  No available slots found'))
            
            # Get recent events
            self.stdout.write(f'\n📋 Recent events (next 7 days):')
            events = calendar_service.get_events(days_ahead=7)
            
            if events:
                for event in events[:5]:  # Show first 5 events
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    summary = event.get('summary', 'No title')
                    
                    if 'dateTime' in event['start']:
                        # Format datetime events
                        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                        start_str = start_dt.strftime('%Y-%m-%d %H:%M')
                        self.stdout.write(f'  📅 {start_str} - {summary}')
                    else:
                        # All-day events
                        self.stdout.write(f'  📅 {start} - {summary} (All day)')
                
                if len(events) > 5:
                    self.stdout.write(f'  ... and {len(events) - 5} more events')
            else:
                self.stdout.write('  No upcoming events found')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Calendar integration is working!'))
            
        except FileNotFoundError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Credentials file not found: {e}')
            )
            self.stdout.write('💡 Run: python manage.py setup_calendar --setup')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )
            self.stdout.write('💡 Check your credentials.json file')
