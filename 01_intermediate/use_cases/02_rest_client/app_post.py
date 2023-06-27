import requests
import json

url = "http://demo6226632.mockable.io/ecs/view-price.sws"

payload = json.dumps([
  {
    "userName": "ETL_BP",
    "token": "116da6a25eb703739d54e3b581ee456d",
    "priceUID": 130047223,
    "productCode": "057/54677",
    "productTypeCode": "ITM",
    "storeId": "3182",
    "supressRegularPriceIfPromotionExist": False,
    "promotionsToInclude": "Simple"
  }
])
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
