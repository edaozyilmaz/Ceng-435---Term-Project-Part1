from socket import *
from threading import Thread
import time

port1 = 26611 #r1 port
sPort = 26614 #s port

linkCosts = [0]*3 #link cost between (r1-r2, r1-d, r1-s)

#r1 is always client
def R1(ip_bind,ip_send,port,temp):
	#receive from s
	count=0
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind((ip_bind,port1))
	while True:
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto("msg",(ip_send, port)) #ip of s
		start = time.time()	#take time to compute link cost
		msg, addr = server.recvfrom(2048)
		end = time.time()
		linkCosts[temp] += end-start
		clientSocket.close()
		#if the received message is "son" break from the while loop because this means it is the end of file
		if(msg=="son"):
			break

	server.close()

#create threads in order to enable multiple requests
t1 = Thread(target=R1, args=('10.10.1.2','10.10.1.1',sPort,2)) #from s to r1, r1 receives
t1.start()
t2 = Thread(target=R1, args=('10.10.8.1','10.10.8.2',26612,0))	#from r2 to r2,r1 sends
t2.start()
t3 = Thread(target=R1, args=('10.10.4.1','10.10.4.2',26610,1))	#from r1 to d,r1 sends
t3.start()
t1.join()
t2.join()
t3.join()

#write link_cost.txt
file_cost = open("linkCost1.txt","w+")
file_cost.write("Link cost of r1 to s: %s \n" % (linkCosts[2]/1000))
file_cost.write("Link cost of r1 to r2: %s \n" % (linkCosts[0]/1000))
file_cost.write("Link cost of r1 to d: %s \n" % (linkCosts[1]/1000))
