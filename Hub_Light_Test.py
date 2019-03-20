# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 21:08:43 2019

@author: Derek Boutin
"""

# Writing to an excel 
# sheet using Python 
import xlwt 
from xlwt import Workbook 
import socket
import json
import requests
import time

# Workbook is created 
wb = Workbook() 

# add_sheet is used to create sheet. 
sheet1 = wb.add_sheet('Sheet 1') 
i = 1
port = 4000 # port number
host = '192.168.1.2' #ip address of hub

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket
s.bind((host, port)) 

s.listen(5) #listen for max 5 connections
print("Hub listening....")

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

sheet1.write(0, 1, 'Sample #')
sheet1.write(0, 2, 'Light Level')
sheet1.write(0, 3, 'Dim Level')

while True:
    client, address = s.accept()
    print("Connecting with " + str(address))
    
    while client:
        sheet1.write(i, 0, i)
        message = client.recv(1024).decode('UTF-8')
        RequestUrl = topLevelUrl + '/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/level' #this command may not return dim level
        response = session.get(RequestUrl)
        sheet1.write(i, 1, message)
        sheet1.write(i, 2, response)
        i = i + 1
        time.sleep(10)


wb.save('xlwt Light_Level_Data.xls') 
