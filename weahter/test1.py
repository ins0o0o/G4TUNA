from urllib.parse import urlencode, unquote
import requests
import json

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
queryParams = '?' + urlencode(
  {
   "ServiceKey" : unquote ("b%2Bl6KbUYclc3AGqxHPCMqoAzo9Ql1Ue5x1pMRYhlOHjemB%2F4JOTQET7PUq7xy6hsR%2Fp1hseiDNohfO2MwEVzyQ%3D%3D"),
                "base_date" : "20241003", 
                "base_time" : "0100",
                "nx" : 61,
                "ny" : 126,
                "numOfRows" : "10",
                "pageNo" : "1",
                "dataType" : "JSON"
        }
)
queryURL = url + queryParams
response = requests.get(queryURL)
print("=== response json data start ===")
print(response.text)
print("=== response json data end ===")
print()

r_dict = json.loads(response.text)
r_response = r_dict.get("response")
r_body = r_response.get("body")
r_items = r_body.get("items")
r_item = r_items.get("item")

result = {}
result2 ={}
for item in r_item:
        if(item.get("category") == "T1H"):
                result = item
                break
for item in r_item:
        if(item.get("category") == "RN1"):
                result2 = item
                break

print("=== response dictionary(python object) data start ===")
print(result.get("baseTime")[:-2] +" temp : " + result.get("obsrValue") + "C")
print(result2.get("baseTime")[:-2] +" rain : " + result2.get("obsrValue") + "mm")
print("=== response dictionary(python object) data end ===")
print()
