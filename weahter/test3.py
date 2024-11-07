import requests
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'base_date': '20241107',
    'base_time': '1300',
    'nx': '61',
    'ny': '126'
}

response = requests.get(url, params=params)

# 응답 상태 코드 확인
if response.status_code != 200:
    print("요청 실패:", response.status_code)
else:
    # XML 데이터 파싱
    root = ET.fromstring(response.content)
    
    # 오류 메시지 확인
    result_code = root.find('.//resultCode')
    result_msg = root.find('.//resultMsg')
    if result_code is not None and result_msg is not None:
        print("오류 코드:", result_code.text)
        print("오류 메시지:", result_msg.text)
    
    # 현재 온도 찾기
    for item in root.iter('item'):
        category = item.find('category').text
        if category == 'T1H':  # T1H는 기온(온도)을 의미함
            temperature = item.find('obsrValue').text
            print(f"현재 온도: {temperature}°C")
            break
