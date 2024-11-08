import requests
from datetime import datetime

def get_calendar_events(calendar_id):
    # Google API Key
    google_key = "AIzaSyA2KUAo4fugxxjo4zG2iHMy1FS70zbls8A"
    
    # Set today's date and calculate start and end times in RFC3339 format
    today = datetime.utcnow().date()
    start_time = f"{today}T00:00:00Z"
    end_time = f"{today}T23:59:59Z"
    
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
        
        # Check if there are any events and print them
        if not events:
            print("오늘 일정은 없습니다.")
        else:
            print("오늘의 일정:")
            for event in events:
                start_time = event.get("start", {}).get("dateTime", "").split("T")[1][:5]
                title = event.get("summary", "제목 없음")
                print(f"{start_time} - {title}")
    else:
        print("Error:", response.status_code, response.text)

# Example usage
calendar_id = input("Enter the calendar ID: ")
get_calendar_events(calendar_id)
