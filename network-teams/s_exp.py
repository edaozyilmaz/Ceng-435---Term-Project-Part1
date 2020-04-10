
from socket import*
from threading import Thread
import time #to take starting time
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
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind((ip,ports))	#bind port s to r3
	clientSocket  = socket(AF_INET, SOCK_DGRAM)
	start=time.time() #take the time as a first message
	startt=str(start)
	clientSocket.sendto(startt.encode(),(s_ip, port)) #send time to r3
	msg, add =server.recvfrom(2048)	#take feedback from r3
	i=0
	while(i<999): #sen 999 more messages to send 1000 message in total
		clientSocket.sendto("a".encode(),(s_ip, port)) #sebnd dummy messages to r3
		i=i+1
		msg, add =server.recvfrom(2048) #receive feedback from r3
	server.close()
	clientSocket.close()
#create threads
t3 = Thread(target=totalSource, args=(ipTable[2],sTable[2],26613))
t3.start()
t3.join()
