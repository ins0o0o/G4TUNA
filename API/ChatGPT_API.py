import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import openai

# 오늘 날짜를 자동으로 가져와 필요한 형식으로 사용
today_date = datetime.today().strftime('%Y%m%d')  # YYYYMMDD 형식
today_date_hyphen = datetime.today().strftime('%Y-%m-%d')  # YYYY-MM-DD 형식

# Google API Key
google_key = "AIzaSyA2KUAo4fugxxjo4zG2iHMy1FS70zbls8A"
openai.api_key = "YOUR_OPENAI_API_KEY"  # OpenAI API 키를 입력하세요

# ChatGPT API를 사용하여 일정 제목에 따른 준비물을 추천
def recommend_supplies(event_title):
    messages = [
        {"role": "system", "content": "당신은 사용자가 일정 제목에 따라 준비물을 추천해주는 도우미입니다."},
        {"role": "user", "content": f"다음 일정 제목에 따른 준비물을 추천해주세요: '{event_title}'. 최대 2개의 준비물을 추천해주세요."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 응답에서 준비물 추출
    recommendations = response['choices'][0]['message']['content'].strip()
    return recommendations

# Google Calendar 일정 가져오기 및 준비물 추천
def get_calendar_events(calendar_id):
    today = datetime.utcnow().date()
    start_time = f"{today}T00:00:00Z"
    end_time = f"{today}T23:59:59Z"

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    params = {
        "key": google_key,
        "timeMin": start_time,
        "timeMax": end_time,
        "singleEvents": "true",
        "orderBy": "startTime"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get("items", [])
        if not events:
            print("오늘 일정은 없습니다.")
        else:
            print("오늘의 일정 및 추천 준비물:")
            for event in events:
                start_time = event.get("start", {}).get("dateTime", "").split("T")[1][:5]
                title = event.get("summary", "제목 없음")
                
                # ChatGPT API를 사용하여 준비물 추천
                supplies = recommend_supplies(title)
                
                print(f"{start_time} - {title}")
                print(f"추천 준비물: {supplies}")
    else:
        print("Error:", response.status_code, response.text)

# 통합 실행
calendar_id = input("캘린더 ID를 입력하세요: ")
print("\n일정 정보:")
get_calendar_events(calendar_id)
