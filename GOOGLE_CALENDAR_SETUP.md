# 🗓️ Google Calendar Integration Setup Guide

## Overview
This integration allows users to see real-time availability from your Google Calendar and book services based on available time slots.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Set Up Google Calendar API
```bash
python manage.py setup_calendar --setup
```

### 3. Configure Google Cloud
1. Go to: https://console.cloud.google.com/
2. Create project or select existing
3. Enable Calendar API: https://console.cloud.google.com/apis/library/calendar.googleapis.com
4. Create OAuth credentials: https://console.cloud.google.com/apis/credentials
5. Download JSON and save as `credentials.json`

### 4. Edit Credentials
Edit `credentials.json` and replace placeholders:
- `YOUR_CLIENT_ID_HERE` → Your actual client ID
- `YOUR_PROJECT_ID_HERE` → Your project ID  
- `YOUR_CLIENT_SECRET_HERE` → Your client secret

### 5. Test Authentication
```bash
python manage.py test_calendar_auth
```

### 6. Configure Settings
Add to `settings.py`:
```python
# Google Calendar Configuration
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
```

## 📋 Features Implemented

### ✅ **Availability Display**
- Shows next 14 days of available slots
- Groups availability by date
- Displays up to 3 slots per day with "more" indicator
- Responsive card-based layout

### ✅ **Smart Booking Integration**
- Click any time slot to pre-fill booking form
- Automatically maps time to appropriate time window
- Shows pre-selected time on booking page

### ✅ **Error Handling**
- Graceful fallback when calendar unavailable
- Clear error messages for users
- No impact on other functionality

### ✅ **Working Hours Support**
- Configurable working hours per day
- Respects closed days
- Minimum 30-minute slot requirements

## 🔧 How It Works

### **Calendar Service** (`services/google_calendar.py`)
- Handles OAuth authentication
- Fetches events from Google Calendar
- Calculates available slots based on working hours
- Finds gaps between existing events

### **View Integration** (`pages/views.py`)
- Fetches availability when loading car care page
- Groups slots by date for template rendering
- Handles calendar errors gracefully

### **Template Display** (`templates/pages/car_care.html`)
- Responsive availability cards
- Click-to-book functionality
- Beautiful styling with hover effects

### **Booking Form** (`templates/bookings/car_care_booking.html`)
- Pre-fills date and time from calendar selection
- Shows selected time to user
- Maintains all existing functionality

## 🎨 UI/UX Features

### **Availability Cards**
- Clean, modern design with gradients
- Hover animations and transitions
- Responsive layout (4-3-2 columns)
- Clear date and time display

### **User Experience**
- One-click booking from calendar
- Visual feedback for selections
- Mobile-friendly interface
- Loading states and error handling

## 📅 Calendar Management

### **Setting Up Your Calendar**
1. Create events in Google Calendar for busy times
2. Set working hours in Django settings
3. Add recurring events for regular bookings
4. Use event titles to describe booking types

### **Best Practices**
- Block time for travel between appointments
- Add buffer time between bookings
- Use color-coding for different service types
- Set up recurring events for regular clients

## 🔍 Testing

### **Test Authentication**
```bash
python manage.py test_calendar_auth --days 7
```

### **Test Calendar Display**
1. Visit `/car-care/` page
2. Check availability section appears
3. Verify time slots are clickable
4. Test booking form pre-fill

### **Test Error Handling**
1. Rename `credentials.json` to test error state
2. Verify graceful error message
3. Ensure other features still work

## 🚨 Troubleshooting

### **Common Issues**

**"Credentials file not found"**
- Run: `python manage.py setup_calendar --setup`
- Complete Google Cloud setup steps
- Ensure `credentials.json` is in project root

**"Authentication failed"**
- Check client ID and secret in credentials.json
- Verify redirect URI matches Google Cloud settings
- Delete `token.json` and re-authenticate

**"No available slots"**
- Check your Google Calendar has events
- Verify working hours configuration
- Ensure calendar isn't set to "private"

**"Calendar temporarily unavailable"**
- Check internet connection
- Verify Google Calendar API is enabled
- Check API quota limits

### **Debug Mode**
Add to settings for debugging:
```python
DEBUG = True
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'services.google_calendar': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Advanced Features

### **Multiple Calendars**
```python
GOOGLE_CALENDAR_ID = 'calendar_1@group.calendar.google.com'
# or use different calendars per service
```

### **Custom Working Hours**
```python
CALENDAR_WORKING_HOURS = {
    'monday': {'start': '08:00', 'end': '18:00'},
    'tuesday': {'start': '08:00', 'end': '18:00'},
    # ... customize per day
}
```

### **Service-Specific Availability**
- Different calendars per service type
- Variable slot durations per service
- Custom buffer times between appointments

## 🎯 Next Steps

1. **Set up Google Calendar API** - Follow the quick setup steps
2. **Test the integration** - Use the test commands
3. **Configure your calendar** - Add working hours and events
4. **Customize styling** - Adjust colors and layout
5. **Monitor performance** - Check API usage and response times

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all setup steps are completed
3. Test with the provided management commands
4. Check Google Cloud Console for API errors

---

**🎉 Congratulations!** Your Rinex Shine website now has real-time calendar integration for improved booking experience!
