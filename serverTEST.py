##server code for CS188 DDoS project
import time, os, sys, string, threading, math
from socket import *  #importing the socket library for network connections

class Server():
  def __init__(self, host, port):
    self.host = host
    self.port = port

    self.num_connections = 0
    self.num_connects_last_interval = 0
    self.avg_connects_per_interval = 0
    self.num_intervals = 0
    self.ddos_detected = 0
    BUFFER_SIZE = 20

    #Creating socket object
    self.serv = socket(AF_INET,SOCK_STREAM)

    #bind socket to address
    self.serv.bind((self.host, self.port))
    self.serv.listen(1) #Setting up the max number of connections we allow as 2, since we want this to be a weak server
    print 'Server up and running! Listening for incomming connections...'


    conn, addr = self.serv.accept()
    print 'Connection address:', addr

    while 1:
      data = conn.recv(BUFFER_SIZE)
      if not data: break
      print "received data:", data
      conn.send(data)  # echo

  def collectData(self):
    threading.Timer(3.0, self.collectData).start()
    self.num_intervals += 1
    print "num connections in last interval", self.num_connects_last_interval
    self.avg_connects_per_interval = ((self.avg_connects_per_interval * (self.num_intervals-1)) + self.num_connects_last_interval) / self.num_intervals
    print "avg connections per interval", self.avg_connects_per_interval
    errorBound = self.avg_connects_per_interval * self.marginOfError(self.num_intervals, 1.96) #95% conf level
    self.checkBound(errorBound)
    self.num_connects_last_interval = 0

  def marginOfError(self, sampleSize, critValue):
    margin = critValue/(2 * math.sqrt(sampleSize))
    return margin

  def checkBound(self, error):
    if self.num_connects_last_interval > self.avg_connects_per_interval + error and self.ddos_detected == 0:
      print "DDOS WARNING"
      self.ddos_detected = 1
    elif self.num_connects_last_interval > self.avg_connects_per_interval + error and self.ddos_detected > 0:
      print "DDOS DETECTED! ERROR:", self.ddos_detected
      self.ddos_detected += 1
    else:
      self.ddos_detected = 0
    print "error bound:", error

  def acceptConnections(self):
    conn, addr = self.serv.accept() ## accept incoming connection
    print 'Connected by ', addr, 'Number of connections: ', self.num_connections
    self.num_connects_last_interval += 1
    self.num_connections += 1
    conn.send('THIS MESSAGE WAS SENT FROM THE SERVER')

##Setting up variables
HOST = '10.1.1.50'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 2048

if __name__ == '__main__':
  victimServer = Server('localhost', 8080)

  victimServer.collectData()

  while 1:
    victimServer.acceptConnections()

#conn.close()
