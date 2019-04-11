import socket
import requests
import json
import threading
import mysql.connector
import json
import numpy as np
from math import sqrt
from collections import Counter

def clientConn(name, conn):
    global RSSI_1
    global RSSI_2
    global RSSI_3
    global ID1
    global ID2
    global ID3
    
    ID = conn.recv(1).decode('UTF-8')
    rssi = conn.recv(50).decode('UTF-8')
    #print(ID)
    if (str(ID) == '1'): 
        RSSI_1 = rssi
        ID1 = True
        #print("1 " + str(ID1))
        print(str(ID) + "   " + str(rssi))

    elif (str(ID) == '2'):
        RSSI_2 = rssi
        ID2 = True
        print(str(ID) + "   " + str(rssi))

    elif (str(ID) == '3'):
        RSSI_3 = rssi
        ID3 = True
        #print("3 " + str(ID3))
        print(str(ID) + "   " + str(rssi))


def openDB():
           con = mysql.connector.connect(user='root', password='Dart2589!',
                              host='127.0.0.1',
                              database='KNN_test')
           return con

def insertExtraRoomRSSI(RSSI_1, RSSI_2, RSSI_3):
    conn = openDB()
    cursor = conn.cursor()
    query = ("INSERT INTO extra_room (ID, RSSI_1, RSSI_2, RSSI_3) VALUES (NULL, %s, %s, %s)")
    query1 = (RSSI_1, RSSI_2, RSSI_3)
    cursor.execute(query, query1)
    conn.commit()
    cursor.close()
    conn.close()

def insertBedRoomRSSI(RSSI_1, RSSI_2, RSSI_3):
    conn = openDB()
    cursor = conn.cursor()
    query = ("INSERT INTO bed_room (ID, RSSI_1, RSSI_2, RSSI_3) VALUES (NULL, %s, %s, %s)")
    query1 = (RSSI_1, RSSI_2, RSSI_3)
    cursor.execute(query, query1)
    conn.commit()
    cursor.close()
    conn.close()

def insertLivingRoomRSSI(RSSI_1, RSSI_2, RSSI_3):
    conn = openDB()
    cursor = conn.cursor()
    query = ("INSERT INTO living_room (ID, RSSI_1, RSSI_2, RSSI_3) VALUES (NULL, %s, %s, %s)")
    query1 = (RSSI_1, RSSI_2, RSSI_3)
    cursor.execute(query, query1)
    conn.commit()
    cursor.close()
    conn.close()

def getExtraRoom():
    conn = openDB()
    cursor = conn.cursor()
    query = ("SELECT RSSI_1, RSSI_2, RSSI_3 FROM extra_room")
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    if (data == None):
        return None
    return data

def getBedRoom():
    conn = openDB()
    cursor = conn.cursor()
    query = ("SELECT RSSI_1, RSSI_2, RSSI_3 FROM bed_room")
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    if (data == None):
        return None
    return data

def getLivingRoom():
    conn = openDB()
    cursor = conn.cursor()
    query = ("SELECT RSSI_1, RSSI_2, RSSI_3 FROM living_room")
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    if (data == None):
        return None
    return data


def sensor_module_conn():
    port = 4000 # port number
    host = '192.168.1.27' #ip address of hub

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket
    s.bind((host, port)) 

    s.listen(5) #listen for max 5 connections
    print("Hub listening....")
    print(threading.active_count())
    while True:
        client, address = s.accept()
        address = str(address)
        print("Connecting with " + str(address))
        
        t = threading.Thread(target=clientConn, args=("clientThread", client))
        #print(threading.active_count())
        t.start()

def createDataSet():
    data = getExtraRoom()

    extra_room_list = []
    bed_room_list = []
    living_room_list = []

    for n in data:
        extra_room_list.append(n)

    data = getBedRoom()
    for n in data:
        bed_room_list.append(n)
        
    data = getLivingRoom()
    for n in data:
        living_room_list.append(n)

    dataset = {'extra-room': extra_room_list, 'bedroom': bed_room_list, 'living-room': living_room_list}
    return dataset

def k_nearest_neighbor(data, predict, k):
    distances = []
    for group in data:
        for features in data[group]:
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance, group]) 

    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]
    return vote_result

def lightControl(name, room):
    port = 5000
    address = '192.168.1.23'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((address, port))
    
    s.send(room.encode('utf-8'))
    s.close()

#Constants For Distance caluclation with RSSI fromula
dataset = createDataSet()

ID1 = False
ID2 = False
ID3 = False
RSSI_1 = 0
RSSI_2 = 0
RSSI_3 = 0 
conn = threading.Thread(target=sensor_module_conn)
conn.start()

k = 3



while True:
    if (ID1 == True and ID2 == True and ID3 == True):
        #print(dataset)
        new_RSSI = []

        ##insert into database here
        
        new_RSSI.append(int(RSSI_1))
        new_RSSI.append(int(RSSI_2))
        new_RSSI.append(int(RSSI_3))

        insertExtraRoomRSSI(RSSI_1, RSSI_2, RSSI_3)
        #print(new_RSSI)

        #print("Here")
        #print(RSSI_1)
        #print(RSSI_2)
        #print(RSSI_3)
        

        result = k_nearest_neighbor(dataset, new_RSSI, k)

        #print(result)
        #print(type(result))
        hub = threading.Thread(target=lightControl, args=("Send to Hub", result))
        hub.start()
        del new_RSSI[:]
        ID1 = False
        ID2 = False
        ID3 = False



