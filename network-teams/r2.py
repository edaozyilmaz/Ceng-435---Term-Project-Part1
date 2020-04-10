from socket import *
from threading import Thread
import time

portr2 = 26612 #r2 port
sPort = 26614 #s port

linkCosts = [0]*2 #link cost between (r2-d, r2-s)

#r2 client to s and d, server to r1 and r3
def R2_client(ip_bind,ip_send,port,temp):
	#receive from s
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind((ip_bind,portr2))
	while True:
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

def R2_server(ip_bind,ip_send,port,temp):
	with open("deneme.txt") as f:
		#split lines to read them one by one
		lines = f.read().splitlines()
		#traverse ipTable to get ip's of r1, r2, and r3
		server = socket(AF_INET, SOCK_DGRAM)
		server.bind((ip_bind,portr2)) 	#bind port S to ipTable
		for line in lines: 	#traverse all of the lines on the .txt file
			msg, add = server.recvfrom(2048)
			clientSocket  = socket(AF_INET, SOCK_DGRAM)
			clientSocket.sendto(line.encode(),(ip_send, port))	#send line to sTable[i] from port S
			clientSocket.close()
		clientSocket  = socket(AF_INET, SOCK_DGRAM)
		#send message "son" to determine the end of the file in order to break fromm while True loop
		clientSocket.sendto("son".encode(),(ip_send, port))
		clientSocket.close()
		server.close()


#create threads in order to enable multiple requests
t1 = Thread(target=R2_client, args=('10.10.2.1','10.10.2.2',sPort,1))	#from s to r2
t1.start()
t2 = Thread(target=R2_client, args=('10.10.5.1','10.10.5.2',26610,0))	##from d to r2
t2.start()
t3 = Thread(target=R2_server, args=('10.10.8.2','10.10.8.1',26611,2))	#from r2 to r1
t3.start()
t4 = Thread(target=R2_server, args=('10.10.6.1','10.10.6.2',26613,3))	#from r2 to r3
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()


#write link_cost.txt
file_cost = open("linkCost2.txt","w+")
file_cost.write("Link cost of r2 to s: %s \n" % (linkCosts[1]/1000))
file_cost.write("Link cost of r2 to d: %s \n" % (linkCosts[0]/1000))
