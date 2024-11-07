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
    
    # 서울 지역 정보 출력
    for item in root.iter('item'):
        station_name = item.find('station_name')
        
        # sidoName이 서울일 때만 출력
        if station_name is not None and station_name.text == '서울':
            station_name = item.find('stationName').text if item.find('stationName') is not None else "N/A"
            pm10_value = item.find('pm10Value').text if item.find('pm10Value') is not None else "N/A"
            data_time = item.find('dataTime').text if item.find('dataTime') is not None else "N/A"
            
            print(f"측정 시간: {data_time}")
            print(f"지역: {station_name}")
            print(f"미세먼지(PM10) 농도: {pm10_value} µg/m³")
            print("-" * 30)
else:
    print("요청 실패:", response.status_code)
