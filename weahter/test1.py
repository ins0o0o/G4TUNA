import requests
import xml.etree.ElementTree as ET

# API URL 및 파라미터 설정
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': 'b%2Bl6KbUYclc3AGqxHPCMqoAzo9Ql1Ue5x1pMRYhlOHjemB%2F4JOTQET7PUq7xy6hsR%2Fp1hseiDNohfO2MwEVzyQ%3D%3D',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'base_date': '20210628',
    'base_time': '0600',
    'nx': '61',
    'ny': '126'
}

# API 요청
response = requests.get(url, params=params)

# XML 파싱
root = ET.fromstring(response.content)

# 온도(T1H) 정보 추출 및 출력
for item in root.iter('item'):
    category = item.find('category').text
    if category == 'T1H':  # T1H는 기온 항목
        temp = item.find('obsrValue').text
        print(f"현재 온도: {temp}°C")
