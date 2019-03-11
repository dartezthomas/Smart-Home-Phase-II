import requests
import json

#exact?level=40

#response = requests.get( 'http://127.0.0.1:8083/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/on', cookies=cookies)
#print(response)

topLevelUrl = 'http://127.0.0.1:8083'
LoginUrl = topLevelUrl + '/ZAutomation/api/v1/login'
username = 'admin'
password = 'laurensellers'

LoginHeader = {'User-Agent': 'Mozilla/5.0', 'Cotent-Type': 'application/json'}
Formlogin = '{"form": true, "login": "'+username+'", "password": "'+password+'", "keepme": false, "default_ui": 1}'

session = requests.Session()
session.post(LoginUrl, headers=LoginHeader, data=Formlogin)

RequestUrl = topLevelUrl + '/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/exact?level=40'
response = session.get(RequestUrl)
print(response)
