import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5006
 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)
 
while True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print ("received message: ", data, " from: ", addr)
    except:
        continue
