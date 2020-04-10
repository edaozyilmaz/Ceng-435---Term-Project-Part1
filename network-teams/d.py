from socket import *
from threading import Thread
import time # for cost

r1ToD = "10.10.4.2"	#ip from r1 to d
r2ToD = "10.10.5.2" #ip from r2 to d
r3ToD = "10.10.7.1" #ip from r3 to d

D1 = "10.10.4.1"	#ip from r1 to d
D2 = "10.10.5.1" #ip from r2 to d
D3 = "10.10.7.2" #ip from r3 to d

portd = 26610	#port d

def totalSource(ip,s_ip,port):
	#take .txt file named deneme.txt
	with open("deneme.txt") as f:
		#split lines to read them one by one
		lines = f.read().splitlines()
		#traverse ipTable to get ip's of r1, r2, and r3
		server = socket(AF_INET, SOCK_DGRAM)
		server.bind((ip,portd)) 	#bind port S to ipTable
		for line in lines: 	#traverse all of the lines on the .txt file
			msg, add =server.recvfrom(2048)
			clientSocket  = socket(AF_INET, SOCK_DGRAM)
			clientSocket.sendto(line.encode(),(s_ip, port))	#send line to sTable[i] from port S
			clientSocket.close()
		clientSocket  = socket(AF_INET, SOCK_DGRAM)
		#send message "son" to determine the end of the file in order to break fromm while True loop
		clientSocket.sendto("son".encode(),(s_ip, port))
		clientSocket.close()
		server.close()


#create threads in order to enable multiple requests
int = 0
t1 = Thread(target=totalSource, args=(r1ToD,D1,26611))
t1.start()
t2 = Thread(target=totalSource, args=(r2ToD,D2,26612))
t2.start()
t3 = Thread(target=totalSource, args=(r3ToD,D3,26613))
t3.start()
t1.join()
t2.join()
t3.join()
