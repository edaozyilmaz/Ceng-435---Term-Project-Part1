from socket import*
from threading import Thread

ipTable = [0]*3
ipTable[0] = '10.10.1.1' #ip of r1
ipTable[1] = '10.10.2.2' #ip of r2
ipTable[2] = '10.10.3.1' #ip of r3

sTable = [0]*3
sTable[0] = '10.10.1.2' #from s to r1
sTable[1] = '10.10.2.1' #from s to r2
sTable[2] = '10.10.3.2' #from s to r3

ports = 26614 #port of s

def totalSource(ip,s_ip,port):
	#take .txt file named deneme.txt
	with open("deneme.txt") as f:
		#split lines to read them one by one
		lines = f.read().splitlines()
		#traverse ipTable to get ip's of r1, r2, and r3
		server = socket(AF_INET, SOCK_DGRAM)
		server.bind((ip,ports)) 	#bind port S to ipTable
		for line in lines: 	#traverse all of the lines on the .txt file
			msg, add = server.recvfrom(2048)
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
t1 = Thread(target=totalSource, args=(ipTable[0],sTable[0],26611))
t1.start()
t2 = Thread(target=totalSource, args=(ipTable[1],sTable[1],26612))
t2.start()
t3 = Thread(target=totalSource, args=(ipTable[2],sTable[2],26613))
t3.start()
t1.join()
t2.join()
t3.join()
