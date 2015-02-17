##Client code for DDoS Project
from socket import * 

HOST = 'localhost'
PORT = 8080
ADDRE = (HOST,PORT)
BUFFSIZE = 2048

client = socket(AF_INET,SOCKSTREAM)
client.connect((ADDR))

data = client.recv(BUFSIZE)
print data

client.close()

