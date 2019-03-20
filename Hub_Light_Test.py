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

sheet1.write(0, 1, 'Sample #')
sheet1.write(0, 2, 'Light Level')

while True:
    client, address = s.accept()
    print("Connecting with " + str(address))
    
    while client:
        sheet1.write(i, 0, i)
        message = client.recv(1024).decode('UTF-8')
        sheet1.write(i, 1, message)
        i = i + 1


wb.save('xlwt Light_Level_Data.xls') 
