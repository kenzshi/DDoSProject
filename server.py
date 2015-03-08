##server code for CS188 DDoS project
import time, os, sys, string, threading, math
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
num_connects_last_interval = 0
avg_connects_per_interval = 0
num_intervals = 0

def collectData():
  threading.Timer(3.0, collectData).start()
  global num_intervals
  num_intervals += 1
  global num_connects_last_interval
  print "num connections in last interval", num_connects_last_interval
  global avg_connects_per_interval
  avg_connects_per_interval = ((avg_connects_per_interval * (num_intervals-1)) + num_connects_last_interval) / num_intervals
  print "avg connections per interval", avg_connects_per_interval
  errorBound = avg_connects_per_interval * marginOfError(num_intervals, 1.96) #95% conf level
  checkBound(errorBound)
  num_connects_last_interval = 0

def marginOfError(sampleSize, critValue):
  margin = critValue/(2 * math.sqrt(sampleSize))
  return margin

def checkBound(error):
  global avg_connects_per_interval
  global num_connects_last_interval
  if num_connects_last_interval > avg_connects_per_interval + error:
    print "DDOS WARNING!!"
  print "error bound:", error
  

collectData()
while 1:
  conn, addr = serv.accept() ## accept incoming connection
  print 'Connected by ', addr, 'Number of connections: ', n
  num_connects_last_interval += 1
  n += 1
  conn.send('THIS MESSAGE WAS SENT FROM THE SERVER')

#conn.close()

