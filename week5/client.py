import requests

url = "http://172.21.10.252:5000/tlqkf"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print("error")