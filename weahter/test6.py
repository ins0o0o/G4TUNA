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
        uv_value = int(uv_index.text)  # 자외선 수치를 정수로 변환
        print("자외선 수치 (h3):", uv_value)

        # 자외선 수치에 따른 문구 출력
        if uv_value >= 3:
            print("선크림을 바르세요.")
        elif uv_value in [1, 2]:
            print("햇빛을 만끽하세요.")
    else:
        print("자외선 수치를 찾을 수 없습니다.")
