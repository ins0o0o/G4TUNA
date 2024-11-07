
import requests
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
params = {
    'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'returnType': 'xml',
    'numOfRows': '100',
    'pageNo': '1',
    'searchDate': '2024-11-07',
    'InformCode': 'PM10'
}

response = requests.get(url, params=params)

# 응답 확인
if response.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response.content)
    
    # 미세먼지 예보 정보 출력
    for item in root.iter('item'):
        inform_data = item.find('informData').text  # 예보 날짜
        inform_grade = item.find('informGrade').text  # 예보 등급 (좋음, 보통, 나쁨 등)
        inform_overall = item.find('informOverall').text  # 종합 예보 설명
        
        print(f"예보 날짜: {inform_data}")
        print(f"예보 등급: {inform_grade}")
        print(f"예보 설명: {inform_overall}")
        print("-" * 30)
else:
    print("요청 실패:", response.status_code)
