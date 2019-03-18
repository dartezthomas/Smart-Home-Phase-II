import socket
import requests
import json
import threading
from scipy import optimize
from numpy import math

def distance_to_wearable(lon1, lat1, lon2, lat2):
    x_dist = abs(lon1-lon2)
    y_dist = abs(lat1-lat2)
    distance = math.sqrt((x_dist)**2 + (y_dist)**2)
    #print("Distance: ", distance)
    return distance

def distance(locations, wearable_location):
    distances = []
    for location, wearable in zip(locations,wearable_location):
        distances.append(distance_to_wearable(location[0],location[1], wearable[0], wearable[1]))
         
    return distances

def RSSI_Distance(r, A, n):
    rssi = int(r)
    exp = -1*((rssi + A)/(10*n))
    result = math.pow(10, exp)
    r = result * 3.281 #convert to feet
    return r

def great_circle_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    #print(lon1, lat1, lon2, lat2)
    x_dist = abs(lon1-lon2);
    y_dist = abs(lat1-lat2);
    distance = math.sqrt((x_dist)**2 + (y_dist)**2)
    return distance

def mse(x, locations, distances):
	mse = 0.0
	for location, distance in zip(locations, distances):
		distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1])
		mse += math.pow(distance_calculated - distance, 2.0)
	return mse / 3


def deviceController(command):
    topLevelUrl = 'http://127.0.0.1:8083'
    LoginUrl = topLevelUrl + '/ZAutomation/api/v1/login'
    username = 'admin'
    password = 'laurensellers'

    LoginHeader = {'User-Agent': 'Mozilla/5.0', 'Cotent-Type': 'application/json'}
    Formlogin = '{"form": true, "login": "'+username+'", "password": "'+password+'", "keepme": false, "default_ui": 1}'

    session = requests.Session()
    session.post(LoginUrl, headers=LoginHeader, data=Formlogin)

    RequestUrl = topLevelUrl + '/ZAutomation/api/v1/devices/ZWayVDev_zway_3-0-38/command/' + command
    response = session.get(RequestUrl)
    print(response)


def clientConn(name, conn):
    global RSSI_1
    global RSSI_2
    global RSSI_3
    global ID1
    global ID2
    global ID3
    
    ID = conn.recv(10).decode('UTF-8')
    rssi = conn.recv(50).decode('UTF-8')
    
    if (str(ID) == '1'): 
        RSSI_1 = rssi
        ID1 = True
        print("1 " + str(ID1))
    elif (str(ID) == '2'):
        RSSI_2 = rssi
        ID2 = True
        print("2 " + str(ID2))
    elif (str(ID) == '3'):
        RSSI_3 = rssi
        ID3 = True
        print("3" + str(ID3))
   



def sensor_module_conn():
    port = 4000 # port number
    host = '192.168.1.5' #ip address of hub

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket
    s.bind((host, port)) 

    s.listen(5) #listen for max 5 connections
    print("Hub listening....")
    print(threading.active_count())
    while True:
        client, address = s.accept()
        print("Connecting with " + str(address))

        t = threading.Thread(target=clientConn, args=("clientThread", client))
        t.start()

        
initial_location = (0,0)

locations = [(0,0), (-14,0), (0,14)]
module_distances=[]

#Constants For Distance caluclation with RSSI fromula
n = 3.772626
A = 64

i = 0
ID1 = False
ID2 = False
ID3 = False
RSSI_1 = 0
RSSI_2 = 0
RSSI_3 = 0 
conn = threading.Thread(target=sensor_module_conn)
conn.start()

while True:
    if (ID1 == True and ID2 == True and ID3 == True):
        print("Here")
        RSSI_1int = int(RSSI_1)
        RSSI_2int = int(RSSI_2)
        RSSI_3int = int(RSSI_3)
        print("1 " + str(RSSI_1int))
        print("2 " + str(RSSI_2int))
        print("3 " + str(RSSI_3int))
        rssi1_dist = RSSI_Distance(RSSI_1int, A, n)
        rssi2_dist = RSSI_Distance(RSSI_2int, A, n)
        rssi3_dist = RSSI_Distance(RSSI_3int, A, n)
        
        module_distances.append(rssi1_dist)
        module_distances.append(rssi2_dist)
        module_distances.append(rssi3_dist)
        
        for i in module_distances:
            print(i)
        
        
        result = optimize.minimize(
        	mse,                         # The error function
        	initial_location,            # The initial guess
        	args=(locations, module_distances), # Additional parameters for mse
        	method='L-BFGS-B',           # The optimisation algorithm
        	options={
        		'ftol':1e-5,         # Tolerance
        		'maxiter': 1e+7      # Maximum iterations
        	})
        location = result.x
        print("x-coordinate: ", location[0])
        print("y-coordinate: ", location[1])
        ID1 = False
        ID2 = False 
        ID3 = False
        del module_distances[:]









            
