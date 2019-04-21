import socket
import uuid
from pynput import keyboard
import time
from player import player
from game import game
from threading import Thread
import selectors

UDP_IP = "172.25.39.37"
 
selector = selectors.DefaultSelector()
UDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP.bind((UDP_IP, 5006))
UDP.listen()
UDP.setblocking(0)
selector.register(UDP, selectors.EVENT_READ, data = None)

# (ip_address, port_num, player_username)
player1 = player("1.11", 1, "shiji's a bitch")
player2 = player("2.22", 2, "fuck you shinji, you whingeing bastard")
# dictionary lookups faster than iterating through a list objects
# probably going to use this instead of the object for storing information
player_list = [player1, player2]
player_dict = {player1.ip : [player1.port, player1.username], player2.ip : [player2.port, player2.username]}

# (game_id, player1_id, player2_id)
game1 = game(uuid.uuid4(), player1.ip, player2.ip)
games_list = [game1]
games_dict = {game1.id : [game1.player1, game1.player2]}

# add a new visitor to the server as a player
def add_player(ip, port_num):
    try:
        player_dict[ip]
        return 0    # if the ip already exists in the dictionary, then return 0
    except:
        player_dict[ip] = [port_num, ""] # if the ip is new, add it to the dictionary
        return 1

# send a username request message to the specified user
def add_username(player_ip, player_port, player_id):
    message = "UR: "
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

# update username for given user
def receive_username(player_ip, player_username):
    try:
        player_dict[player_ip][1] = player_username
    except:
        send_error(player_ip, "")

# send lobby information and direct to lobby
def send_lob_info(player_ip, player_port):
    message = "TL:{0}".format(len(player_dict))
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

# disconnect user (delete player from player list)
def disconnect(user_id):
    for p in player_list:
        if p.id == user_id:
            player_list.remove(p)

# let the client know that the connection has been rejected
def reject_conn(ip, port, msg):
    message = "RJ:{0}".format(msg)
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (ip, port))
    sock.close()

# let the client know that the connection has been accepted
def accept_conn(ip, port):
    message = "AC: "
    smessage = str.encode(message)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto(smessage, (ip, port))
    # sock.close()
    print(smessage)

# general error message sender
def send_error(ip,port,msg):
    message = "ER:{0}".format(msg)
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (ip, port))
    sock.close()

# retrieve information from port, send to correct game, lobby, etc.
# format is "{2 Character message type}:field1,field2,field3,...."
def direct_traffic(message, ip, port):
    msg_type = message[:2]
    msg = message[3:]
    if msg_type == "LR": # logon request
        print(msg_type)
        new_player = add_player(ip,port)
        
        if not new_player:
            reject_conn(ip, port, "Another player with the same ip has alread joined."
                            "New connection denied.")
        else:
            accept_conn(ip,port)

    elif msg_type == "SU": # send username
        print(msg_type)
        username, user_id = msg.split(',')
        for p in player_list:
            if p.id == user_id:
                p.set_username(username)
    elif msg_type == "SM": # send move
        print(msg_type)
        game_id, user_id, move = msg.split(',')
        game_found = false
        for game in games_list:
            if game.id == game_id:
                if move == "u":
                    game.move_up(user_id)
                elif move == "d":
                    game.move_down(user_id)
                else:
                    send_error(ip,port,"Invalid move sent.")
                game_found = true
                break
        if not game_found:
            send_error(ip,port,"Game not found.")
    elif msg_type == "QR": # quit or rematch
        print(msg_type)
        game_id, user_id, option = msg.split(',')
    elif msg_type == "BM": # begin matchmaking
        print(msg_type)
        user_id = msg
    elif msg_type == "DC": # disconnect
        print(msg_type)
        user_id = msg
    else:
        print(message)


if __name__ == "__main__":
    #print(UDP.getsockname())
    #while True:
    #    try:
    #        data, addr = UDP.recvfrom(4096) # buffer size is 1024 bytes
    #        #addr, port = UDP.accept()
    #        t_addr, port = addr
    #        print ("received message:", data, " from ", t_addr, " : ", port)
    #        direct_traffic(data.decode("utf-8"), t_addr, port)
    #    except:
    #        continue

    direct_traffic("LR", "1.1.1.1", 5006)