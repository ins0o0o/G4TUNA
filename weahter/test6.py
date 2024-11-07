import requests
import xml.etree.ElementTree as ET

url = 'https://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
params = {
    'ServiceKey': 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'XML',
    'areaNo': 'seoul',
    'time': '20241107'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    # 자외선 수치 정보 출력
    for item in root.iter('item'):
        area_name = item.find('areaNo').text if item.find('areaNo') is not None else "N/A"
        uv_index = item.find('h3').text if item.find('h3') is not None else "N/A"  # h3 태그가 자외선 지수

        if area_name == 'seoul':
            print(f"지역: {area_name}")
            print(f"자외선 수치 (h3): {uv_index}")
            break
else:
    print("요청 실패:", response.status_code)
