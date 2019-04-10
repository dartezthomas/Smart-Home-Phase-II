import urllib
import requests
import json
import os
import subprocess

#print('Status of Light')

#response = urllib.request.urlopen('http://http://192.168.1.2:8083/ZWaveAPI/Run/SerialAPIGetInitData(0)')
x = "http://127.0.0.1:8083/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/exact?level=40"
y = "cookie.txt"
#/ZWaveAPI/Run/devices[3].instances[0].commandClasses[0x25].Set(255)')
subprocess.Popen('cmd')
print(s)
headers = {
    'Accept': 'application/json'
    }


resp = urllib.request.Request('http://127.0.0.1:8083/ZAutomation/api/v1/status', headers=headers)

response_body = urllib.request.urlopen(resp).read()
print(response_body.decode('UTF-8'))

#print(type(response_body))

#resp1 = urllib.request.Request('http://127.0.0.1:8083/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/on', headers=headers)

#response_body1 = urllib.request.urlopen(resp1).read()

#data = json.dumps(response_body1.decode('UTF-8'))
#print(type(data))
#print(data)
