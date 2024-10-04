import requests
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'base_date': '20241004',
    'base_time': '1200',
    'nx': '61',
    'ny': '126'
}

response = requests.get(url, params=params)

# XML 데이터 파싱
root = ET.fromstring(response.content)

# 현재 온도 찾기
for item in root.iter('item'):
    category = item.find('category').text
    if category == 'T1H':  # T1H는 기온(온도)을 의미함
        temperature = item.find('obsrValue').text
        print(f"현재 온도: {temperature}°C")
        break
