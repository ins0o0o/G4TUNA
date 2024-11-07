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
    
    # 미세먼지 예보 정보 출력 (서울만)
    for item in root.iter('item'):
        inform_data = item.find('informData').text  # 예보 날짜
        inform_grade = item.find('informGrade').text  # 지역별 예보 등급
        inform_overall = item.find('informOverall').text  # 종합 예보 설명

        # 서울 정보만 출력
        if '서울' in inform_grade:
            # 서울에 해당하는 등급 정보 추출
            grade_info = [info for info in inform_grade.split(', ') if '서울' in info]
            seoul_grade = grade_info[0] if grade_info else "정보 없음"
            
            print(f"예보 날짜: {inform_data}")
            print(f"서울 미세먼지 등급: {seoul_grade}")
            print(f"예보 설명: {inform_overall}")
            print("-" * 30)
else:
    print("요청 실패:", response.status_code)
