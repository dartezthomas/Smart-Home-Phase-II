import mysql.connector #sudo apt-get install python3-mysql.connector
import socket
import requests
import json
import threading
import numpy as np
from math import sqrt
from collections import Counter
import matplotlib.pyplot as plt
import time

#Run KNN Localization Code Here:


def openDB():
           con = mysql.connector.connect(user='Smart_Home_user', password='laurensellers',
                              host='127.0.0.1',
                              database='Smart_Home_db')
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

def insertMachineLearningLightData(old_light, new_level):
    conn = openDB()
    cursor = conn.cursor()
    query = ("INSERT INTO light_learning(ID, x_value, y_value) VALUES (NULL, %s, %s, %s)")
    query1 = (old_light, new_level)
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

def Least_Squares(room):
    conn = openDB()
    cursor = conn.cursor()
    x_coords, y_coords = [],[]
    # execute the SQL query using execute() method.
    if (room == 'extra-room'):
        query = "SELECT x_values_lux, y_values_coords from light_learning_extra_room"
        cursor.execute(query)
        # fetch all of the rows from the query
        data = cursor.fetchall()
        # print the rows
        for row in data:
            x_coords.append(row[0])
            y_coords.append(row[1])
            
    if (room == 'bedroom'):
        query = "SELECT x_values_lux, y_values_coords from light_learning_bed_room"
        cursor.execute(query)
        # fetch all of the rows from the query
        data = cursor.fetchall()
        # print the rows
        for row in data:
            x_coords.append(row[0])
            y_coords.append(row[1])
    
    if (room == 'living-room'):
        query = "SELECT x_values_lux, y_values_coords from light_learning_living_room"
        cursor.execute(query)
        # fetch all of the rows from the query
        data = cursor.fetchall()
        # print the rows
        for row in data:
            x_coords.append(row[0])
            y_coords.append(row[1])
            
    cursor.close()
    conn.close()
    x = np.array(x_coords)
    y = np.array(y_coords)
    new_y = 100-y
    
    '''
    This is to account for the positive slope that results from using thea lgrithm;
    need to change this back when ready for the final values
    '''
    b = estimate_coef(x, new_y)
    #print("Estimated Coeficients:\nm = {} \ \ny-int= {}".format(b[1], b[0]))
    m = b[1]
    y_int = b[0]
    #plotting regression line
    plot_regression_line(x, new_y,b)
    
    return m,y_int
    
def hub_conn():
    port = 6000 # port number
    
    host = '192.168.1.30' #ip address of cloud
    
    dataset = createDataSet()
    k = 3
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket
    s.bind((host, port)) 

    s.listen(5) #listen for max 5 connections
    #print("Hub listening....")
    #print(threading.active_count())
    print("Cloud Listening...")
    while True:
        client, address = s.accept()
        address = str(address)
        print("Connecting with " + str(address))

        jsonReceived = client.recv(1024).decode('UTF-8')

        dataRecevied = json.loads(jsonReceived)
        RSSI_data =[]
        for data in dataRecevied:
            RSSI_data.append(data['RSSI'])

       
        print(dataRecevied)
        #print(dataset)
        light_level = dataRecevied[0]
        #should be the light level parsed from received data of ID 1
        light = light_level['light_level']
        RSSI_array = list(map(int, RSSI_data))
        print(RSSI_array)
        #print(type(RSSI_data))
        print("Light Level: " + light)
                
        room_prediction = k_nearest_neighbor(dataset, RSSI_array, k)
        print(room_prediction)
        
        #Use Machine Learning to create/add to learned light levels
        old_light,new_level = machine_learning_light(light,room_prediction)
        insertMachineLearningLightData(old_light, new_level)
        
        '''
        in this section of the code needs to have to output of Least Squares
        part and store the output in a varaible to be sent to the hub. 
         
        '''
        m,y_int = Least_Squares(room)
        
        output = light*(m) + (y_int)        
        output_level = 100 - output
        
        client.send(output_level.encode('utf-8'))
        client.close()
        
        #client.send(output.encode('utf-8'))
        #client.close()
            
        
        

#add light learning functions here
#########################
        
def machine_learning_light(light,room):
    if (light == old_light):
        i = i+1
        if(i==3):
            RequestURL = topLevelUrl+'/ZAutomation/api/v1/devicews/ZWayVDev_zway_10-0-38/command/update'
            response = session.get(RequestUrl)
            response = session.get(RequestUrl) #Called a second time to send it back to be outputted in the shell
            RequestUrl_1 = topLevelUrl + '/ZAutomation/api/v1/devices/ZWayVDev_zway_10-0-38'
            response = session.get(RequestUrl_1)
            r = session.put(RequestUrl_1)
            res = json.loads(response.text)
            new_level = res['data']['metrics']['level']
            if (new_level!=old_level and room != old_room):
                time.sleep(20) #Wait 20 seconds before capturing the new light level
                response = session.get(RequestUrl)
                response = session.get(RequestUrl)
                RequestUrl_1 = topLevelUrl + '/ZAutomation/api/v1/devices/ZWayVDev_zway_10-0-38'
                response = session.get(RequestUrl_1)
                r = session.put(RequestUrl_1)
                res = json.loads(response.text)
                new_level = res['data']['metrics']['level']
                
                if (room == 'extra-room'):
                    #Use database here instead of opening a file
                    '''
                    light_data = open("Light Data.txt", "a")
                    str_original_light = str(original_light)
                    light_data.write(str_original_light + "\n") #x-coordinate
                    string_level = str(new_level)
                    light_data.write(string_level + "\n") #y-coorindate
                    light_data.close()
                    '''
                    #The first line of this file is the original light level (x-coordinate)
                    #The second line of this file is the dim level (y-coordinate)
                    #This pattern repeats throughout
                    
                if (room == 'bed-room'):
                    #Use database here instead of opening a file
                    '''
                    light_data = open("Light Data.txt", "a")
                    str_original_light = str(original_light)
                    light_data.write(str_original_light + "\n") #x-coordinate
                    string_level = str(new_level)
                    light_data.write(string_level + "\n") #y-coorindate
                    light_data.close()
                    '''
                    #The first line of this file is the original light level (x-coordinate)
                    #The second line of this file is the dim level (y-coordinate)
                    #This pattern repeats throughout
                    
                if (room == 'living-room'):
                    #Use database here instead of opening a file
                    '''
                    light_data = open("Light Data.txt", "a")
                    str_original_light = str(original_light)
                    light_data.write(str_original_light + "\n") #x-coordinate
                    string_level = str(new_level)
                    light_data.write(string_level + "\n") #y-coorindate
                    light_data.close()
                    '''
                    #The first line of this file is the original light level (x-coordinate)
                    #The second line of this file is the dim level (y-coordinate)
                    #This pattern repeats throughout
                    
                    

                old_level = new_level
                old_room = room
                #End of if statement
            else:
                new_level = None    
            original_light = light
            i=0
        else:
            i=0
        old_light = light
        
        #To ensure old_light value is None if new_level is None:
        if (new_level == None):
            old_light = None
        
    return old_light,new_level

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

def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 

    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 

    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x - n*m_y*m_x) 
    SS_xx = np.sum(x*x - n*m_x*m_x) 

    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 

    return(b_0, b_1)

def plot_regression_line(x, y, b): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 

    # predicted response vector 
    y_pred = b[0] + b[1]*x 

    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
      # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 

    # function to show plot 
    plt.show()

#Constants For Distance caluclation with RSSI fromula

def main():
    
k = 3
old_message = 0
old_light = 0
old_level = 0
old_room = ''
i = 0
x_coords = []
y_coords = []
conn = threading.Thread(target=hub_conn)
conn.start()




'''
while True:
    #if (ID1 == True and ID2 == True and ID3 == True): This will be done on the hub
        #print(dataset)
        new_RSSI = []
        ##insert into database here
        
        new_RSSI.append(int(RSSI_1))
        new_RSSI.append(int(RSSI_2))
        new_RSSI.append(int(RSSI_3))
        #insertLivingRoomRSSI(RSSI_1, RSSI_2, RSSI_3)
        #print(new_RSSI)
        #print("Here")
        #print(RSSI_1)
        #print(RSSI_2)
        #print(RSSI_3)
        
        #Machine Learning Localization:
        result = k_nearest_neighbor(dataset, new_RSSI, k)
        print(result)
        #print(type(result))
        #Sending Location to Central Hub
        hub = threading.Thread(target=lightControl, args=("Send to Hub", result))
        hub.start()
        del new_RSSI[:]
        ID1 = False
        ID2 = False
        ID3 = False
To connect to the database, use the following commands:
conn = openDB()
cursor = conn.cursor()
query = ("INSERT INTO <table> (<INFO>)
query1 = (<DATA>)
cursor.execute(query, query1)
conn.commit()
cursor.close()
conn.close()
'''











'''
previous_room = ''
current_room = room (from KNN Localization Code)
Combine Hub_Light_Test(1).py code with the code below
if previous_room != current_room:
    if (current_room=='extra-room'):
       open database
       record light level (lux)
       store in table
       delay 30 seconds
       record state of switch
       store in table
    else:
       do nothing
else:
    do nothing
'''
main()