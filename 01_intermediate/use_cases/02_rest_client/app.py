import requests

url = "http://demo6226632.mockable.io/api/v1/getcomppids/checkItem?formatType=sears&product=17-26597"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
