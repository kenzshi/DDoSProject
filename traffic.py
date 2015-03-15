#!/usr/bin/python
import time, random, socket, os, sys, string

host='10.1.1.50'
port=8080
message='asdf'
conn=input("How many connections do you want to make: ")
ip = socket.gethostbyname(host)
n = 0
def generate_traffic():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("GET /%s HTTP/1.1\r\n" % message)
  except socket.error, msg:
    global n
    n = n+1
    print("|[Connection Failed] | %d", n )
  print ("|[Message Sent] |")
  s.close()

while(1):
    generate_traffic()
    time.sleep(random.uniform(0.01,0.025))
