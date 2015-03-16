Team 3: Kacey Ryan, Jeffrey Wang, Kenny Shi, Calvin Chan
CS188 Distributed Systems
DDoS With Detection Analysis

## LIBRARIES:

_NTP_ - Used for Python time synchronization
_Impacket_ - Used for python packet manipulation (Changing Source IP/ Setting Packet Flags)
_scapy_ - Used for python packet manipulation (Changing Source IP/ Setting Packet Flags)

To install libraries:
scapy - enter directory scapy-2.2.0: cd scapy-2.2.0
        install library:             sudo python setup.py install

NTP - make sure ntplib.py is included in the home directory; all files that use ntp already have the import included

Impacket - enter directory: cd impacket-0.9.11
        install library: sudo python setup.py install

## CODE:

`basic_slave.py` - This is a simple slave that we created to make actual connections to the server with local detection. It does not run syn flood, it makes full connections. The code runs on an infinite loop as it is currently setup, however we have the option to have it run for a designated number of packets. This was used for some testing of the local detection.

`client.py` - This is our simple client script that makes a single connection to the server to make sure it is still up and running during DDoS. This was used during testing of our syn flood.

`generator.py` - This is a random traffic generator that utilizes scapy to modify the source IP addresses of packets. The packets are able to be sent and reach the server, however they cannot be seen by our server.py script so it could only be used for testing and data by utilizing tcpdump.

`ipflush.sh` - This is a script to wipe IPTABLES

`master.py` - Our main master node code. This code syncs up with the slaves and controls the slaves to launch an attack. When the master is launched, it waits around for the slaves to connect. Once all the slaves (in our case 3) have connected, the master will calculate a time offset and order all the slaves to attack at the same time.

`ntplib.py` - library for ntp, which we use for time sync

`ntplib.pyc` - compiled library for ntp

`scapy_syn_flood.py` - This is a synflood attack that is implemented utilizing scapy. After setting IPTABLES on the attack nodes to prevent sending reset packets: sudo iptables -A OUTPUT -p tcp -s <slave_IP> --tcp-flags RST RST -j DROP
and setting IPTABELS on the server to limit connetions: sudo iptables -A INPUT -p tcp --syn --dport 8080 -m connlimit --connlimit-above <num_connections> -j REJECT
this shows that we can crash the server node. Unfortunately, these packets cannot be identified by our server.py program so we cannot analyze these packets.

`server.py` - This is our main server that looks at attempted connections and runs local detection alongside working like a normal server. It does message parsing and attempts to serve as many clients as it can. We limit this server using IPTABLES when we do our syn flood attack to cause it to fail.

`slave.py` - The slave code, and the heart of our botnet. The slaves take a time argument as well as a victim server, and launches a DoS attack on the victim server. Each slave spawns new threads of the attack to parallelize them, and sends spoofed SYN packets to DoS the victim. 

`spoof.py` - Testing code for spoofing IP Addresses using Scapy as well as IMPacket libraries

`spoofslave.py` - Integration of spoofed IP address code with our slave code

`traffic.py` - This is a traffic generator created for testing our server. It does not utilize scapy or spoof IP addresses so our server can identify it's connections. This was used to create random traffic flow to our server while testing local detection. There is a random sleep time that can be altered in the program that can change the traffic flow from light to heavy to inconsistent traffic if necessary. I utilized this to show all of the different conditions our local detection performs in.

`data_logs` - This directory contains all of our outputted data when running our tests for local detection. All of this data eventually was used to make the graphs that are in the appendices of our report.

`backscatter_data` - This directory contains all of our outputted data for backscatter analysis. This includes the pure tcpdump that we used, as well as various parsed data files in other formats (json,csv). In addition, we’ve also included the parsing scripts to transform the tcpdump into other formats, as well as the actual local analysis code to perform the analysis on the DDoS attacks.

## DEMONSTRATION:

_Master/Slave Attack_

    - Start server: Run `python server.py` on the server node ($server node, as listed in the ns file). This must be done on the $server node, since this is the server to be attacked.
    - Start master: Run `python master.py` on the master node ($control node, as listed in the ns file). This must be done on the $control node, since that is the node the slaves connect to.
    - Connect Slaves: After the master is running, connect the slaves by running `./slave.py` on $bot1, $bot2, and $bot3 sequentially. Slaves will automatically connect to the master machine if using the DETER lab environment. 
    - The attack will now commence once three bots have connected to the master. For the sake of the demo, the attack is not meant to run on forever.

## LOCAL DETECTION TESTS:

    - Start Traffic Generation: python traffic.py (after setting the amount of traffic you want inside the code's sleep parameter)
    - Start the server: python server.py
    - Let the code run for a few intervals to allow the average and the error bounds to settle.
    - Run Attack: python basic_slave.py (I used basic slave to ensure I had control over the time intervals manually. You could run the entire master slave if necessary)
    - Watch the server flag all of the out of bounds packet counts
    - Stop Attack: CTRL-C (Watch the server begin to readjust average and error)
    - Rinse and Repeat as necessary!

## BACKSCATTER TESTS:

    - Start Traffic Generation: python traffic.py (after setting the amount of traffic you want inside the code's sleep parameter)
    - Start the server: python server.py
    - Start the tcpdump: tcpdump -i eth3 -an
    - Start the master: python master.py
    - Start the bots: python spoofslave.py
    - Watch the tcpdump as it monitors all packets being sent and received
    - Parse the tcpdump data into json or csv: parse_data_to_json.py | parse_data_to_csv.py
    - Run the analysis on the data (after specifying minimum time delta in code): flow_analysis.py



