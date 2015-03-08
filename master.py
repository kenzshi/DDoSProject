import time, datetime, sys, re, socket
class Master():
  def __init__(self, sock=None):
    if sock is None:
      self.sock = socket(AF_INET, SOCK_STREAM)
    else:
      self.sock = sock
    self.slaves = {}

  def connectionListen(self, port):
    print "Listening for connections"
    self.sock.bind('localhost', port)
    self.sock.listen(5)

  def connectionAccept(self, port):
    print('Accepting connection from port: {0}'.format(port))

if __name__ == '__main__':
    port = 8080
    masterServer = Master()
    masterServer.connectionListen(port)
