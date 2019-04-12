import socket
import uuid

#UDP_IP = "172.25.39.37"
 
#UDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#UDP.bind(('', 0));

player_list = [("1","1234","123123123"), ("123", "234","456")]    # (ip_address, player_id, player_name)

for x,y,z in player_list:
    print(x)

while True:

     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     print ("received message:", data)

def add_player():
    for (address, id, name) in player_list:
        if address == addr:
            return 0
    player_list.append((address,uuid.uuid1(),""))