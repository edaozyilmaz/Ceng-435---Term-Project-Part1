from socket import *
from threading import Thread
import time
import os

portr3 = 26613 #r3 port
sPort = 26614 #s port

def r3():
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('10.10.3.2',portr3))  #bind port r3 to s
	i=0
	while i<1000: 	#take 1000 messages from s and send them to the d
		msg, addr = server.recvfrom(2048) 	#take message from s
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto("msg",('10.10.3.1', sPort)) #send feedback to s
		clientSocket.close()
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto(msg,('10.10.7.1', 26610)) #send the messages coming from s to d
		clientSocket.close()
		server1 = socket(AF_INET, SOCK_DGRAM)
		server1.bind(('10.10.7.2',portr3))	#bind port r3 to d
		msg, addr = server1.recvfrom(2048) 	#take feedback from d
		server1.close()
		i=i+1
	server.close()


#create thread
t1 = Thread(target=r3, args=())
t1.start()
t1.join()
