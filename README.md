#DDOS Project

Implementation of a DDoS botnet as well as DDoS detection tools, tested on the DETERLabs systems.

##Team Members:
* Calvin Chan
* Kacey Ryan
* Kenny Shi
* Jeffrey Wang

#CS188 Midterm Report: DDoS Project

###Introduction

The distributed denial of service (DDoS) project will be divided into two parts. One part is the implementation of a botnet for use in DDoS of a specified server at a synchronized time. The second part of the project involves the detection of such DDoS attacks with analysis of their precision and accuracy of identifying the attack. The first method of detection is backscatter which utilizes the botnets IP spoofing to identify false packets. The second method is network flow analysis which recognizes anomalies in network behavior, whether it be spikes in traffic or an abnormal number of dropped packets. Once implemented, we will run data analysis and testing to compare and contrast detection methods as well as observe them separately to understand their strengths and weaknesses.
	
###DDoS Implementation Design

![DDoS Implementation Design](https://raw.githubusercontent.com/kenzshi/DDoSProject/master/DDOSMockup.png)

The implementation of our DDoS network consists of three important parts:
* **Botnet** - The botnet will be responsible for carrying out the attack on a server. It consists of a master/slave configuration of computers:
* **Master** - The “main” machine in the DDoS attack, the master node will be in charge of sending to and receiving messages from the slave to coordinate the attack. The master node will also perform the time synchronization of the other nodes to make sure that the attack happens at the same time.
* **Slaves** - These will be the mindless drones in our attack. Using DETERLab’s environment, we will spin up a number of these slaves that will be controlled by the master node. These slave nodes will receive messages from the master and flood the victim server with packets.
* **Control** - A regular node (not part of the botnet) that connects to the server normally. This node will be used as a reference point to compare connection performance against the other nodes that are actually involved in the DDoS attack. It will be used in our analysis to help us figure out the irregularities in the network as a result of the attack. 
* **Server** - node in which all other nodes will connect and send requests to. The server must be implemented in such a way that a specified, weak number of connections will bring it down.

As these three entities interact with each other and carry out a DDoS attack, we will be able to analyze the attacks to compare and contrast the different types of detection.

###Technical Design

For the technical aspects of the design, we will be writing the majority of the code in Python. The code will be distributed to machines provided to us by DETERLab. The components of our project are as follows:
* **server.py**: Poor implementation of a server, since we want it to be easily DDoS’d with only a few machines (due to DETERLab limits)
* **analysis.py**: Implementation of our two detection methods as well as performance analysis code
* **master.py**: Takes care of time syncronization and communication between the slave machines
* **slave.py**: Reports information to master.py and listens for attack information, floods target with HTTP GET requests, and spoofs IP 
* **control.py**: Very simple client that sends requests to our server

###Time Synchronization

An important portion of our design relies on the time synchronization between the slave.py nodes. In order for us to have a successful DDoS, we want all the slave machines to send the packets at the same time. Since the machine times might differ, our solution to time synchronization is to use the Network Time Protocol (NTP) to have the slaves sync up with our master. Since we’re writing in Python, we will be using the ntplib package(4) to help with any time sync issues. We thought of other methods of doing the time synchronization, but the methods involved propagation delay/transmission delay of packets, and we felt it was too low-level for us to work with. As the TA suggested, we looked into the NTP and decided to use that instead.

###Detection Methods

###Backscatter

One of the most well-known methods of detecting DDoS attacks is through backscatter analysis. In a DDoS attack, a common technique used is IP spoofing, in which attackers will randomly spoof their IP address in attempts to mask the actual attacks themselves. As such, when the victim host receives what appears to be a valid request (SYN) from one of the spoofed IP addresses, it responds correspondingly with a correct response (SYN/ACK) for that request.

Backscatter analysis works by monitoring a specific subset of the Internet addresses that are susceptible to receiving these ghost SYN/ACK packets from the victimized host. By doing so, we can determine the likelihood of a specific flow of requests and responses being a DDoS attack. 

First, we must make several assumptions. Each packet that is received by the victimized host must come from a random source address (models the IP spoofing). Next, we assume that the host responds once per request packet received. Finally, we assume that an attack has a total of m packets.

With our above assumptions, the probability of a given host on the internet receiving an unsolicited response by the victimized host is:
```
	m/2^32
```
If we monitor a subset of n IP addresses, the expectation of observing an attack:
```
	E(x) = nm/2^32 
```
With that, we can actually estimate the actual rate of the attack:
```
	R>=R’ 2^32/n
```
where R’ is the measured average inter-arrival rate of backscatter from the victim, and R is the calculated, extrapolated rate from R’ of the rate of the attack.

With the above calculations, we can monitor the request/response traffic over an extended period of time and identify explicit time frames between which a DDoS might be occurring. One of the accepted ways to do this is through flow based classification of traffic. We can post-process the monitored data and identify series of consecutive packets that share the same target IP address and IP protocol. By identify the first packet as the start of a flow; that flow encapsulates all following packets that are received within a set time delta of the previous packet (say, 5 minutes). We can then filter the flows by the total number of received packets and the total duration of the flow (say, we discard all flows that do not have at least 100 packets and do not last longer than 60 seconds). This way, we essentially filter out the normal traffic that is expected of the victimized host, and isolate the culprit flows that may indicate a DDoS attack.

It is important to note that backscatter analysis has traditionally been done post-processing, not real time. Furthermore, it does not identify the actual culprit of a DDoS attack, but merely identifies specific time frames in which DDoS could be occurring.

###Network Flow Analysis

Besides backscatter, one of the popular detection approaches for DDoS attacks and other malicious network exploits is network flow analysis. The idea behind network flow analysis is very general as it is merely a detection of anomalies in a network’s traffic. This general category can be approached by many subsets of methods whether it be a cluster analysis, covariance analysis, or a more common approach such as traffic spikes. The popularity of network flow as a tool has produced constant improvement in this field. 

Cluster analysis is the isolation of nodes into clusters based on incoming traffic to create a preemptive and proactive act on attacks. (1) Covariance analysis is a more hit and miss method that has shown great levels of predictive accuracy with large amounts of incoming traffic, but is otherwise hard to manage and utilize for smaller networks. (2) These two methods, although they may be more suited for high accuracy and precision, would be very difficult to manage and utilize with minimal resources available. For these reason, we have decided to go with a more basic network analysis method that will merely record patterns of incoming traffic from nodes. Anything off pattern can be marked as an anomaly and too many anomalies will lead to detection.

The data to be noted will be incoming number of packets, number of sockets utilized in time intervals, number of packets from specific IP addresses (this will be more applicable for backscatter), and the number of dropped and received packets in time intervals. These numbers will be useful in detection of the DDoS itself as well as the analysis of the two detection methods separately. 

###Analysis of Implementation

The most important part of this project will be the analysis of the DDoS attack and the two detection methods. After implementation, the majority of our time will go into testing the limits, positives, and negatives of our network detection. We will see where the strengths of backscatter and network flow lie as well as their respective weaknesses. In order to do this, we will utilize our control node to test when the network becomes unaccessible due to the DDoS. We will see how our detection mechanisms respond and how quickly they respond if they do. Measures such as: number of dropped packets/ received packets, percentage of successful connections, as well as false positive detections and false negative detections will be important. (3) We will know the time of the start of the DDoS based on our time synchronization and the control node’s ability to connect. Our detection mechanisms should output a timestamp of when they detected the attack. All of this data will allow us to improve and eventually create well designed detection mechanisms for our network. Overall, we will be able to see which mechanism would be better in different situations and why one mechanism outperforms the other.

###References
* http://www.sciencedirect.com/science/article/pii/S0957417407000395
* http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1312847
* http://www.gregthatcher.com/Azure/Ch2_DetectingDenialOfService.aspx
* https://pypi.python.org/pypi/ntplib/ 
* http://www.caida.org/publications/papers/2001/BackScatter/usenixsecurity01.pdf
