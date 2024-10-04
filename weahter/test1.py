import requests

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : 'b%2Bl6KbUYclc3AGqxHPCMqoAzo9Ql1Ue5x1pMRYhlOHjemB%2F4JOTQET7PUq7xy6hsR%2Fp1hseiDNohfO2MwEVzyQ%3D%3D', 
         'pageNo' : '1', 
         'numOfRows' : '1000', 
         'dataType' : 'XML', 'base_date' : '20210628', 'base_time' : '0600', 'nx' : '61', 'ny' : '126' }

response = requests.get(url, params=params)
print(response.content)
