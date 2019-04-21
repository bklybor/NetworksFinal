import socket
import uuid
from pynput import keyboard
import time
from player import player
from game import game

UDP_IP = "172.25.39.37"
 
UDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP.bind(('', 0));
UDP.setblocking(0)

# (ip_address, port_num, player_id, player_username)
player1 = player("1.11", 1, "11.1", "shiji's a bitch")
player2 = player("2.22", 2, "22.2", "fuck you shinji, you whingeing bastard")
player_list = [player1, player2]    

# (game_id, player1_id, player2_id)
game1 = game(uuid.uuid4(), player1.id, player2.id)
games_list = [game1]

# add a new visitor to the server as a player
def add_player(ip, port_num):
    for addr, port, id, name in player_list:
        if addr == ip:
            return 0
    player_list.append(player(ip,port_num,uuid.uuid4(),""))
    return 1

# send a username request message to the specified user
def add_username(player_ip, player_port, player_id):
    message = "UR:{0}".format(player_id)
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

# update username for given user
def receive_username(player_ip, player_username):
    for index, (ip, port, id, name) in enumerate(player_list):
        if ip == player_ip:
            player_list[index] = (ip, port, id, player_username)
            print(player_list[index])

# send lobby information and direct to lobby
def send_lob_info(player_ip, player_port):
    message = "TL:{0}".format(len(player_list))
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

# disconnect user (delete player from player list)
def disconnect(user_id):
    for p in player_list:
        if p.id == user_id:
            player_list.remove(p)

# let the client know that the connectio has been rejected
def reject_conn(ip, port, msg):
    message = "RJ:{0}".format(msg)
    smessage = str.encode(message)
    sock = socket.socket(socket.AFT_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (ip, port))
    sock.close()

# let the client know that the connection has been accepted
def accept_conn(ip, port):
    message = "AC: "
    smessage = str.encode(message)
    sock = socket.socket(socket.AFT_INET, socket.SOCK_DGRAM)
    sock. sendto(smessage, (ip, port))
    sock.close()

# general error message sender
def send_error(ip,port,msg):
    message = "ER:{0}".format(msg)
    smessage = str.encode(message)
    sock = socket.socket(socket.AFT_INET, socket.SOCK_DGRAM)
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
                if move == "0":
                    game.move_up(user_id)
                elif move == "1":
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
        print(msg_type)


if __name__ == "__main__":
    while True:
        print(UDP.getsockname())
        try:
            data, addr = UDP.recvfrom(4096) # buffer size is 1024 bytes
            print ("received message:", data)
        except BlockingIOError:
            print("no data yet")
         
         
        time.sleep(1)