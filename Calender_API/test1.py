import requests
from datetime import datetime, timedelta

def get_calendar_events(calendar_id, date):
    # Google API Key
    google_key = "AIzaSyA2KUAo4fugxxjo4zG2iHMy1FS70zbls8A"
    
    # Calculate start and end times in RFC3339 format for the specified date
    start_time = f"{date}T00:00:00Z"
    end_time = f"{date}T23:59:59Z"
    
    # Construct the API URL
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    params = {
        "key": google_key,
        "timeMin": start_time,
        "timeMax": end_time,
        "singleEvents": "true",
        "orderBy": "startTime"
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        events = response.json().get("items", [])
        
        # Print event titles
        print("Events on", date)
        for event in events:
            print(event.get("summary", "No Title"))
    else:
        print("Error:", response.status_code, response.text)

# Example usage
calendar_id = input("Enter the calendar ID: ")
date = input("Enter the date (YYYY-MM-DD): ")
get_calendar_events(calendar_id, date)
