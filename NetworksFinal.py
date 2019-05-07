import socket
import uuid
from pynput import keyboard
import time
from player import player
from game import game
import threading
import selectors

host_ip = "0.0.0.0"
 
# selector = selectors.DefaultSelector()
# the default listening port for incoming logon requests
lst_port = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
lst_port.bind((host_ip, 5006))
# lst_port.listen()
lst_port.setblocking(0)
# selector.register(lst_port, selectors.EVENT_READ, data = None)



# (ip_address, port_num, player_username)
# player1 = player("1.11", 1, "player 1")
# player2 = player("2.22", 2, "player 2")
# dictionary lookups faster than iterating through a list objects
# probably going to use this instead of the object for storing information
player_list = []

# (game_id, player1_id, player2_id)
# game1 = game(uuid.uuid4(), player1.ip, player2.ip)
games_list = []

# update username for given user
def receive_username(player_ip, player_username):
    is_found = False
    for p in player_list:
        if p.ip == player_ip:
            is_found = True
            p.username = player_username

    return is_found

# disconnect user (delete player from player list)
def disconnect(user_id):
    for p in player_list:
        if p.id == user_id:
            player_list.remove(p)

# general function for sending a message to the client
def send_data(ip, port, data):
    smsg = str.encode(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smsg, (ip, port))
    sock.close()

# send a username request message to the specified user
def add_username(player_ip, player_port):
    message = "UR: "
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

# send lobby information and direct to lobby
def send_lob_info(player_ip, player_port):
    message = "TL:{0}".format(len(player_dict))
    smessage = str.encode(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (player_ip, player_port))
    sock.close()

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(smessage, (ip, port))
    sock.close()
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
    print(message)
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
        game_id, move = msg.split(',')
        game_found = False
        print(games_list[0].id)
        for g in games_list:
            if g.id == game_id:
                print("game_found()")
                if move == "u":
                    print(ip, " moving_up()")
                    g.move_up(ip)
                elif move == "d":
                    print(ip, " moving_down()")
                    g.move_down(ip)
                else:
                    print("error")
                    send_error(ip,port,"Invalid move sent.")
                game_found = True
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
    return "done_directing_traffic()"


#def accept_wrapper(sock):
#    conn, addr = sock.accept()
#    print('acceptect connectoin from: ', addr)
#    conn.setblocking(0)
#    data = types.SimpleNamespace(addr = addr, inb = b'', outb = b'')
#    events = selectors.EVENT_READ | selectors.EVENT_WRITE
#    selector.register(conn, events, data = data)

#def service_connection(key, mask):
#    sock = key.fileobj
#    data = key.data
#    if mask & selectors.EVENT_READ:
#        recv_data = sock.recv(1024)
#        if recv_data:
#            data.outb += recv_data
#        else:
#            print('closing connection to: ', data.addr)
#            sel.unregister(sock)
#            sock.close()
#    if mask & selectors.EVENT_WRITE:
#        if data.outb:
#            print('echoing ', repr(data.outb), ' to ', data.addr)
#            sent = sock.send(data.outb)
#            data.outb = data.outb[sent:]

# add a new visitor to the server as a player
# def add_player(ip, port):

def send_game_update(gm, player1, player2):
    print("preparing_message()")
    message = "UG:{0},{1},{2},{3},{4},{5},{6},{7}".format(gm.id, gm.player1_y_pos, gm.player2_y_pos, gm.ball_x_pos, gm.ball_y_pos,  gm.player1_score, gm.player2_score, "0")
    smessage = str.encode(message)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock1.sendto(smessage, (player1.ip, player1.to_port))
    sock2.sendto(smessage, (player2.ip, player2.to_port))
    sock1.close()
    sock2.close()
    print("game_state_update_sent()")
    print(smessage, " sent to ", player1.ip, " and ", player2.ip)

if __name__ == "__main__":
    # print(UDP.getsockname())
    # while True:
    #    events = selector.select(timeout = None)
    #    for key, mask in events:
    #        if key.data is None:
    #            accept_wrapper(key.fileobj)
    #        else:
    #            service_connection(key, mask)

    vinny = player("172.25.23.161", 10500, 5007 , "player 1")
    nick = player("172.25.45.119", 55433, 5008, "player 2")
    gm = game(vinny.ip, nick.ip, "1")

    games_list.append(gm)

    # send_game_update(gm, vinny, nick)

    start_time = time.time()
    cur_time = 0.0
    el_time = 0.0

    while True:

        try:
            data, addr = lst_port.recvfrom(4096) # buffer size is 1024 bytes
            # addr, port = UDP.accept()
            t_addr, port = addr
            print ("received message:", data, " from ", t_addr, " : ", port)
            print(direct_traffic(data.decode("utf-8"), t_addr, port))
            
        except:
            pass

        #cur_time = time.time()
        #el_time = cur_time - start_time
        #print(el_time % 1)

        gm.move_ball()
        send_game_update(gm, vinny, nick)
        time.sleep(0.05)
        
