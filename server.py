##server code for CS188 DDoS project
import time, os, sys, string
from socket import *  #importing the socket library for network connections

##Setting up variables
HOST = '10.1.1.50'
PORT = 8080
ADDR = (HOST,PORT) 
BUFSIZE = 2048

##Creating socket object
serv = socket(AF_INET,SOCK_STREAM)

##bind socket to address
serv.bind((ADDR))
serv.listen(1) ##Setting up the max number of connections we allow as 2, since we want this to be a weak server
print 'Server up and running! Listening for incomming connections...'

n = 1

while 1:
	conn, addr = serv.accept() ## accept incoming connection
	print 'Connected by ', addr, 'Number of connections: ', n
	n += 1
	conn.send('THIS MESSAGE WAS SENT FROM THE SERVER')

#conn.close()

