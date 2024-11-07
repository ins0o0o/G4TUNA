import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# URL과 파라미터 설정
url = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
queryParams = '?' + urllib.parse.urlencode({
    urllib.parse.quote_plus('ServiceKey'): 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    urllib.parse.quote_plus('areaNo'): '1121571000',  # 서울 지역 코드
    urllib.parse.quote_plus('time'): '2024110718',   # 날짜 및 시간 예시
    urllib.parse.quote_plus('dataType'): 'XML'
})

# 요청 생성 및 응답 수신
request = urllib.request.Request(url + queryParams)
with urllib.request.urlopen(request) as response:
    response_body = response.read().decode('utf-8')

    # XML 파싱
    root = ET.fromstring(response_body)
    
    # h3 태그에서 자외선 수치 추출
    uv_index = root.find('.//h3')
    if uv_index is not None:
        print("자외선 수치 (h3):", uv_index.text)
    else:
        print("자외선 수치를 찾을 수 없습니다.")
