import socket

port = 4000 # port number
host = '192.168.1.2' #ip address of hub

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket
s.bind((host, port)) 

s.listen(5) #listen for max 5 connections
print("Hub listening....")

while True:
    client, address = s.accept()
    print("Connecting with " + str(address))
    while client:
        message = client.recv(1024).decode('UTF-8')
        print(message)
        
