import socket
import uuid
from pynput import keyboard
import time
from player import player

UDP_IP = "172.25.39.37"
 
UDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP.bind(('', 0));
UDP.setblocking(0)

# (ip_address, port_num, player_id, player_username)
player1 = player("1.11", 2, "11.1", "shiji's a bitch")
player2 = player("2.22", 2, "22.2", "fuck you shinji, you whingeing bastard")
player_list = [player1, player2]    


def add_player():
    for address, port, id, name in player_list:
        if address == addr:
            return 0
    player_list.append((address,uuid.uuid4(),""))

# send a username request message to the specified user
def add_username(player_ip, player_port):
    message = "Username Request"
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))

# update username for given user
def receive_username(player_ip, player_username):
    for index, (ip, port, id, name) in enumerate(player_list):
        if ip == player_ip:
            player_list[index] = (ip, port, id, player_username)
            print(player_list[index])

# send lobby information
def send_lob_info(player_ip, player_port):
    message = "Current Lobby Size: {0}".format(len(player_list))
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))

# disconnect user (delete player from player list)
def disconnect(user_id):
    for p in player_list:
        if p.id == user_id:
            player_list.remove(p)

# retrieve information from port, send to correct game
# format is "Update Game: game_id, player_id, move"
def direct_traffic():


if __name__ == "__main__":
    while True:
        print(UDP.getsockname())
        try:
            data, addr = UDP.recvfrom(4096) # buffer size is 1024 bytes
            print ("received message:", data)
        except BlockingIOError:
            print("no data yet")
         
         
        time.sleep(1)