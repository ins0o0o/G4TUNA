import requests
import xml.etree.ElementTree as ET
from datetime import datetime

url = 'https://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
params = {
    'ServiceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'pageNo': '1',
    'numOfRows': '10',
    'dataType': 'XML',
    'areaNo': 'seoul',  # 서울 지역 코드 (예시)
    'time': '20241106'
}

response = requests.get(url, params=params)

# 응답 상태 코드 및 XML 파싱
if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    # resultCode 확인
    result_code = root.find('.//resultCode').text
    result_msg = root.find('.//resultMsg').text
    
    if result_code == '00':  # 정상 응답
        # 자외선 수치 정보 출력
        for item in root.iter('item'):
            date = item.find('date').text if item.find('date') is not None else "N/A"
            uv_index = item.find('h3').text if item.find('h3') is not None else "N/A"  # 자외선 지수
            
            print(f"날짜: {date}")
            print(f"자외선 지수: {uv_index}")
    elif result_code == '03':  # NO_DATA 오류
        print("데이터가 없습니다. 요청한 날짜 또는 지역 코드를 확인하세요.")
    else:
        print(f"오류 발생: {result_msg}")
else:
    print("요청 실패:", response.status_code)
