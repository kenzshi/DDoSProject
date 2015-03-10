import time, datetime, sys, re,ntplib
from socket import *  #importing the socket library for network connections
from time import ctime

class Master():
  def __init__(self, sock=None):
    if sock is None:
      self.sock = socket(AF_INET, SOCK_STREAM)
    else:
      self.sock = sock
    self.slaves = {}

    # get ntp times
    self.ntpc = ntplib.NTPClient()
    self.ntp_res = self.ntpc.request('europe.pool.ntp.org', version=3)

  def listenConnections(self, port):
    print "Listening for connections"
    self.sock.bind(('localhost', port))
    self.sock.listen(3)

  def acceptConnections(self):
    conn, addr = self.sock.accept()
    print('Accepting connection {0}'.format(addr))
    print('Conn is {0}'.format(conn))
    msg_buf = conn.recv(64)
    if len(msg_buf) > 0:
      print(msg_buf)
    conn.send('Master offset is: {0}'.format(self.ntp_res.offset))
    self.slaves[addr] = conn

if __name__ == '__main__':
    port = 8081
    masterServer = Master()
    masterServer.listenConnections(port)
    while 1:
      masterServer.acceptConnections()
