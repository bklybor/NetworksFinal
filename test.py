import socket

UDP_IP = "172.25.41.161"
UDP_PORT = 5006
MESSAGE = "Suck my dick Vincent!"
 
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)
SMESSAGE = str.encode(MESSAGE)
   
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.sendto(SMESSAGE, (UDP_IP, UDP_PORT))
