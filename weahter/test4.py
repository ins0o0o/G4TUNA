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

if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    # 날짜별로 서울 정보 저장
    seoul_data = {}

    for item in root.iter('item'):
        inform_data = item.find('informData').text  # 예보 날짜
        inform_grade = item.find('informGrade').text  # 지역별 예보 등급
        inform_overall = item.find('informOverall').text  # 종합 예보 설명

        # 서울 관련 등급 정보만 추출
        if '서울' in inform_grade:
            # 서울 등급 정보 추출
            grade_info = [info for info in inform_grade.split(', ') if '서울' in info]
            seoul_grade = grade_info[0] if grade_info else "정보 없음"
            
            # 날짜별로 서울의 예보 정보를 저장 (마지막 값으로 갱신됨)
            seoul_data[inform_data] = {
                'grade': seoul_grade,
                'overall': inform_overall
            }

    # 날짜별 서울 미세먼지 예보 정보 출력
    for date, data in seoul_data.items():
        print(f"예보 날짜: {date}")
        print(f"서울 미세먼지 등급: {data['grade']}")
        print(f"예보 설명: {data['overall']}")
        print("-" * 30)
else:
    print("요청 실패:", response.status_code)
