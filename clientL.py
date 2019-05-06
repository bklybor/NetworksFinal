from tkinter import *
import socket
import random
import time
# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle, paddle2):
        self.canvas = canvas
        self.paddle = paddle
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.xspeed = 5
        self.yspeed = -1

    def draw(self,x,y):
        self.canvas.move(self.id, x, y)

# paddle 1 functions
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) 
        self.yspeed = 0
        self.canvas.move(self.id, 10, 150)
        self.canvas.bind_all('<KeyPress-Up>', self.move_up)
        self.canvas.bind_all('<KeyPress-Down>', self.move_down)
    def draw(self,x):
        print(x)
        self.canvas.move(self.id,0,x)
    def move_up(self, evt):
        PORT = 5006
        IP = "172.25.40.161"
        MESSAGE = "SM:1,u"
        SMESSAGE = str.encode(MESSAGE)
        print (MESSAGE)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock1.bind(('',5007))
        sock1.sendto(SMESSAGE, (IP, PORT))
    def move_down(self, evt):
        PORT = 5006
        IP = "172.25.40.161"
        MESSAGE = "SM:1,d"
        SMESSAGE = str.encode(MESSAGE)
        print (MESSAGE)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock1.bind(('',5007))
        sock1.sendto(SMESSAGE, (IP, PORT))
class Paddle2:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) # player 2, your opponent!
        self.yspeed = 0
        self.canvas.move(self.id, 480, 150)        
    def draw(self,x):
        self.canvas.move(self.id,0,x)


#Make background and declare colors and design
tk = Tk()
tk.title("Ping")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='white')
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'black')
paddle2 = Paddle2(canvas, 'black')
ball = Ball(canvas, 'black', 25, paddle, paddle2)

UDP_IP = "0.0.0.0"
UDP_PORT = 10500
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

sock.setblocking(0)
is_loss = False
datastring = ""
toParse = ["1","0","0","250","200","0","0","0"]
player1_speed = 0
player1_pos = 150
player2_speed = 0
player2_pos = 150
ball_x_pos = 250
ball_x_speed = 0
ball_y_pos = 200
ball_y_speed = 0
#Game Loop
while is_loss == False:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print ("received message:", data)
        datastring = data.decode("utf-8")
        toParse = datastring.split(",")

        player1_speed = player1_pos - int(toParse[1])
        player2_speed = player2_pos - int(toParse[2])
        print("player2pos: ", player2_pos)
        player1_pos = int(toParse[1])
        player2_pos = int(toParse[2])
        paddle.draw(player1_speed)
        paddle2.draw(player2_speed)

        ball_x_speed = ball_x_pos - int(toParse[3])
        print("ballxspeed : ", ball_x_speed)
        ball_y_speed = ball_y_pos - int(toParse[4])
        print("ballyspeed : ", ball_y_speed)
        ball_x_pos = int(toParse[3])
        ball_y_pos = int(toParse[4])
        ball.draw(toParse[3],toParse[4])
    except:
        pass
    if toParse[7] == "1":
        is_loss = True
    tk.update_idletasks()
    tk.update()
    time.sleep(.01)
#Game Over
gameover_label = canvas.create_text(250,200,text="GAME OVER",font=("Calibri",30))
tk.update()
