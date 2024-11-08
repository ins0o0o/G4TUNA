import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.request
import urllib.parse

# 오늘 날짜를 자동으로 가져와 필요한 형식으로 사용
today_date = datetime.today().strftime('%Y%m%d')  # YYYYMMDD 형식
today_date_hyphen = datetime.today().strftime('%Y-%m-%d')  # YYYY-MM-DD 형식

# Google API Key
google_key = "AIzaSyA2KUAo4fugxxjo4zG2iHMy1FS70zbls8A"

# 1. 현재 온도와 강수확률 가져오기
def get_weather_forecast():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {
        'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': today_date,
        'base_time': '0500',
        'nx': '61',
        'ny': '126'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("기상 예보 요청 실패:", response.status_code)
        return

    root = ET.fromstring(response.content)
    temperature = None
    precipitation_probability = None

    for item in root.iter('item'):
        category = item.find('category').text
        obsr_value = item.find('fcstValue').text

        if category == 'TMP':  # TMP: 1시간 기온
            temperature = obsr_value
        elif category == 'POP':  # POP: 강수확률
            precipitation_probability = int(obsr_value)

    if temperature is not None:
        print(f"현재 온도: {temperature}°C")
    else:
        print("온도 정보를 찾을 수 없습니다.")

    if precipitation_probability is not None:
        print(f"강수확률: {precipitation_probability}%")
        if precipitation_probability > 45:
            print("우산을 챙기세요.")
        else:
            print("맑은 날씨입니다.")
    else:
        print("강수확률 정보를 찾을 수 없습니다.")

# 2. 서울 미세먼지 등급 가져오기
def get_dust_forecast():
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
    params = {
        'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
        'returnType': 'xml',
        'numOfRows': '1',
        'pageNo': '1',
        'searchDate': today_date_hyphen,
        'InformCode': 'PM10'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("미세먼지 예보 요청 실패:", response.status_code)
        return

    root = ET.fromstring(response.content)
    
    for item in root.iter('item'):
        inform_data = item.find('informData').text
        inform_grade = item.find('informGrade').text
        
        if inform_data == today_date_hyphen:
            grade_info = [info.strip() for info in inform_grade.split(',') if '서울' in info]
            seoul_grade = grade_info[0] if grade_info else "정보 없음"
            
            print(f"예보 날짜: {inform_data}")
            print(f"서울 미세먼지 등급: {seoul_grade}")
            
            if "나쁨" in seoul_grade or "매우 나쁨" in seoul_grade:
                print("나쁨 등급입니다. 마스크를 가져가세요.")
            elif "보통" in seoul_grade or "좋음" in seoul_grade:
                print("오늘은 마스크가 없는 하루를 보내세요.")
            break

# 3. 자외선 수치 가져오기
def get_uv_index():
    url = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
    queryParams = '?' + urllib.parse.urlencode({
        urllib.parse.quote_plus('ServiceKey'): 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
        urllib.parse.quote_plus('areaNo'): '1121571000',
        urllib.parse.quote_plus('time'): today_date + '18',
        urllib.parse.quote_plus('dataType'): 'XML'
    })

    request = urllib.request.Request(url + queryParams)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        root = ET.fromstring(response_body)
        
        uv_index = root.find('.//h3')
        if uv_index is not None:
            uv_value = int(uv_index.text)
            print("자외선 수치:", uv_value)

            if uv_value >= 3:
                print("선크림을 바르세요.")
            elif uv_value in [0, 1, 2]:
                print("햇빛을 만끽하세요.")
        else:
            print("자외선 수치를 찾을 수 없습니다.")

# 4. Google Calendar 일정 가져오기
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
            print("오늘의 일정:")
            for event in events:
                start_time = event.get("start", {}).get("dateTime", "").split("T")[1][:5]
                title = event.get("summary", "제목 없음")
                print(f"{start_time} - {title}")
    else:
        print("Error:", response.status_code, response.text)
calendar_id = input("캘린더 ID를 입력하세요: ")

# 통합 실행
print("\n")
get_weather_forecast()
print("\n")
get_dust_forecast()
print("\n")
get_uv_index()

# Google Calendar 일정 조회

print("\n")
get_calendar_events(calendar_id)
