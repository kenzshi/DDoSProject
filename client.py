##Client code for DDoS Project
from socket import * 

HOST = '10.1.1.50'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 2048

client = socket(AF_INET,SOCK_STREAM)
client.connect((ADDR))

data = client.recv(BUFSIZE)
print data

client.close()

