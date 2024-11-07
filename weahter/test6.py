import urllib.request
import urllib.parse

# URL과 파라미터 설정
url = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
queryParams = '?' + urllib.parse.urlencode({
    urllib.parse.quote_plus('ServiceKey'): 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0+jWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA==',
    urllib.parse.quote_plus('areaNo'): '1121571000',  # 서울 지역 코드 (예시)
    urllib.parse.quote_plus('time'): '2024110718',   # 예시 시간: 2022년 07월 11일 18시
    urllib.parse.quote_plus('dataType'): 'XML'
})

# 요청 생성 및 응답 수신
request = urllib.request.Request(url + queryParams)
with urllib.request.urlopen(request) as response:
    response_body = response.read().decode('utf-8')
    print(response_body)
