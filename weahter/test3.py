import requests
import xml.etree.ElementTree as ET

# URL과 파라미터 설정
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params = {
    'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'base_date': '20241107',  # 예보 기준 날짜 (YYYYMMDD 형식)
    'base_time': '0500',       # 예보 기준 시간 (예: 0500은 05:00)
    'nx': '61',                # X 좌표 (서울시)
    'ny': '126'                # Y 좌표 (서울시)
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
        print("")
        print("")
    
    # 예보 데이터를 저장할 변수들
    temperature = None
    precipitation_probability = None

    # 각 요소를 찾아서 저장
    for item in root.iter('item'):
        category = item.find('category').text
        obsr_value = item.find('fcstValue').text  # 예보 값

        if category == 'TMP':  # TMP: 1시간 기온
            temperature = obsr_value
        elif category == 'POP':  # POP: 강수확률
            precipitation_probability = obsr_value

    # 결과 출력
    if temperature is not None:
        print(f"현재 온도: {temperature}°C")
    else:
        print("온도 정보를 찾을 수 없습니다.")

    if precipitation_probability is not None:
        print(f"강수확률: {precipitation_probability}%")
    else:
        print("강수확률 정보를 찾을 수 없습니다.")
