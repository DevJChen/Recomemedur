import os
import time
import requests

response = requests.get("http://api.scraperapi.com?api_key=0eca4ea452573c36b96740d463e4ccf4&url=https://httpbin.org/ip", headers={"User-agent": "scraperapi"})
print(response.text)


