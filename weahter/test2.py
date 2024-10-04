import requests

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : 'gAFYOesD02xHwlm93c35FiqgHKnqAJp6d0%2BjWA3aPcN6DAeVtK22eFtV8gA493BmO4azi7xqk9RY5KdKpeBvTA%3D%3D', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : '20210628', 'base_time' : '0600', 'nx' : '55', 'ny' : '127' }

response = requests.get(url, params=params)
print(response.content)
