from socket import *
from threading import Thread
import time # for cost
import os

portr3 = 26613 #r3 port
sPort = 26614 #s port

linkCosts = [0]*3 #link cost between (r3-r2, r3-d, r3-s)

#r3 is always client
def r3(ip_bind,ip_send,port,temp):
	#receive from s
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind((ip_bind,portr3))
	while True:
		count=0
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto("msg",(ip_send, port)) #ip of s
		clientSocket.close()
		start = time.time()	#take time to compute link cost
		msg, addr = server.recvfrom(2048)
		end = time.time()
		linkCosts[temp] += end-start
		#if the received message is "son" break from the while loop because this means it is the end of file
		if(msg=="son"):
			break
	server.close()


#create threads in order to enable multiple requests
t1 = Thread(target=r3, args=('10.10.3.2','10.10.3.1',sPort,2)) #from s to r3
t1.start()
t2 = Thread(target=r3, args=('10.10.7.2','10.10.7.1',26610,1)) #from r3 to d
t2.start()
t3 = Thread(target=r3, args=('10.10.6.2','10.10.6.1',26612,0)) #from r3 to r2
t3.start()
t1.join()
t2.join()
t3.join()

#write link_cost.txt
file_cost = open("linkCost3.txt","w+")
file_cost.write("Link cost of r3 to s: %s \n" % (linkCosts[2]/1000))
file_cost.write("Link cost of r3 to r2: %s \n" % (linkCosts[0]/1000))
file_cost.write("Link cost of r3 to d: %s \n" % (linkCosts[1]/1000))
