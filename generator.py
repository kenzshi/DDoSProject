#! /usr/bin/python

import random, time
from scapy.all import *

HOST = "10.1.1.50"
PORT = 8080

while(1):
  source = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
  packet = IP(src = source, dst = HOST) / UDP(dport = PORT)
  send(packet, iface='tap2')
  print "Sent packet to:", HOST, "From Source IP:", source
  time.sleep(random.uniform(0,2))
