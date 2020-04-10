from socket import *
from threading import Thread
import time 	#to take ending time

r3ToD = "10.10.7.1" #ip from r3 to d

D3 = "10.10.7.2" #ip from r3 to d

portd = 26610	#port d

def totalSource(ip,s_ip,port):
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind((ip,portd)) 	#bind portd to r3
	i=0
	while i<1000: 	#take 1000 messages
		msg, add =server.recvfrom(2048) 	#take message from r3
		if(msg!="a"):	 #if message is the time take it as starting time
			start = msg.decode("utf-8")
		clientSocket  = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto("msg".encode(),(s_ip, port)) #send feedback to r3
		clientSocket.close()
		i=i+1
	end=time.time()	 #after 1000 messages received take the end time
	st=float(start)
	e2e=end-st 	#calculate end-to-end time
	server.close()
	print e2e

#create thread
t3 = Thread(target=totalSource, args=(r3ToD,D3,26613))
t3.start()
t3.join()
