import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 현재 날짜를 YYYY-MM-DD 형식으로 가져옵니다.
today = datetime.today().strftime('%Y-%m-%d')

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
params = {
    'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'returnType': 'xml',
    'numOfRows': '1',
    'pageNo': '1',
    'searchDate': today,
    'InformCode': 'PM10'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    # 오늘의 서울 미세먼지 정보 출력
    for item in root.iter('item'):
        inform_data = item.find('informData').text  # 예보 날짜
        inform_grade = item.find('informGrade').text  # 지역별 예보 등급
        
        # 서울의 미세먼지 등급만 필터링
        if inform_data == today:
            # '서울'에 대한 정보만 추출
            grade_info = [info.strip() for info in inform_grade.split(',') if '서울' in info]
            seoul_grade = grade_info[0] if grade_info else "정보 없음"
            
            print(f"예보 날짜: {inform_data}")
            print(f"서울 미세먼지 등급: {seoul_grade}")
            break
else:
    print("요청 실패:", response.status_code)
