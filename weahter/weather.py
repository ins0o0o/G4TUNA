import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.request
import urllib.parse

# 오늘 날짜를 자동으로 가져와 필요한 형식으로 사용
today_date = datetime.today().strftime('%Y%m%d')  # YYYYMMDD 형식
today_date_hyphen = datetime.today().strftime('%Y-%m-%d')  # YYYY-MM-DD 형식

# 1. 현재 온도와 강수확률 가져오기
def get_weather_forecast():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {
        'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': today_date,  # 오늘 날짜 (YYYYMMDD 형식)
        'base_time': '0500',       # 예보 기준 시간 (예: 0500은 05:00)
        'nx': '61',                # X 좌표 (서울시)
        'ny': '126'                # Y 좌표 (서울시)
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
        obsr_value = item.find('fcstValue').text  # 예보 값

        if category == 'TMP':  # TMP: 1시간 기온
            temperature = obsr_value
        elif category == 'POP':  # POP: 강수확률
            precipitation_probability = int(obsr_value)  # 정수로 변환하여 비교

    if temperature is not None:
        print(f"현재 온도: {temperature}°C")
    else:
        print("온도 정보를 찾을 수 없습니다.")

    if precipitation_probability is not None:
        print(f"강수확률: {precipitation_probability}%")
        # 강수확률에 따른 메시지 출력
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
        'searchDate': today_date_hyphen,  # 오늘 날짜 (YYYY-MM-DD 형식)
        'InformCode': 'PM10'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("미세먼지 예보 요청 실패:", response.status_code)
        return

    root = ET.fromstring(response.content)
    
    for item in root.iter('item'):
        inform_data = item.find('informData').text  # 예보 날짜
        inform_grade = item.find('informGrade').text  # 지역별 예보 등급
        
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
        urllib.parse.quote_plus('areaNo'): '1121571000',  # 서울 지역 코드
        urllib.parse.quote_plus('time'): today_date + '18',   # 오늘 날짜 (YYYYMMDD) + 시간 (18시)
        urllib.parse.quote_plus('dataType'): 'XML'
    })

    request = urllib.request.Request(url + queryParams)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')

        root = ET.fromstring(response_body)
        
        uv_index = root.find('.//h3')
        if uv_index is not None:
            uv_value = int(uv_index.text)  # 자외선 수치를 정수로 변환
            print("자외선 수치:", uv_value)

            if uv_value >= 3:
                print("선크림을 바르세요.")
            elif uv_value in [0, 1, 2]:
                print("햇빛을 만끽하세요.")
        else:
            print("자외선 수치를 찾을 수 없습니다.")


# 통합 실행

get_weather_forecast()

get_dust_forecast()

get_uv_index()
