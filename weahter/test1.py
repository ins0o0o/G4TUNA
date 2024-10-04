import requests
import xml.etree.ElementTree as ET

# API URL 및 파라미터 설정
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': 'b%2Bl6KbUYclc3AGqxHPCMqoAzo9Ql1Ue5x1pMRYhlOHjemB%2F4JOTQET7PUq7xy6hsR%2Fp1hseiDNohfO2MwEVzyQ%3D%3D',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'base_date': '20241003',  # 유효한 날짜인지 확인 필요
    'base_time': '0600',       # 유효한 시간인지 확인 필요
    'nx': '61',
    'ny': '126'
}

# API 요청
response = requests.get(url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    print("API 요청 성공!")
else:
    print(f"API 요청 실패. 상태 코드: {response.status_code}")
    print(f"응답 내용: {response.content}")

# XML 파싱
try:
    root = ET.fromstring(response.content)

    # 온도(T1H) 정보 추출 및 출력
    found = False
    for item in root.iter('item'):
        category = item.find('category').text
        if category == 'T1H':  # T1H는 기온 항목
            temp = item.find('obsrValue').text
            print(f"현재 온도: {temp}°C")
            found = True

    if not found:
        print("온도 정보(T1H)를 찾을 수 없습니다.")

except ET.ParseError as e:
    print(f"XML 파싱 오류: {e}")
except Exception as e:
    print(f"에러가 발생했습니다: {e}")
