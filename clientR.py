import socket
from pynput import keyboard
from tkinter import *
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

    def draw(self, x, y):
        pos = self.canvas.coords(0, int(x), int(y))


# Define paddle properties and functions
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) 
        self.yspeed = 0
        self.canvas.move(self.id, 10, 150 )


    def draw(self, x):
        y = int(x)
        pos = self.canvas.coords(0, 480, y)
        

class Paddle2:
    def __init__(self, canvas, color):
       self.canvas = canvas
       self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) 
       self.yspeed = 0
       self.canvas.move(self.id, 480, 150)
       self.canvas.bind_all('<KeyPress-Up>', self.move_up2)
       self.canvas.bind_all('<KeyPress-Down>', self.move_down2)

    def draw(self, x):
        y = int(x)
        print ("Converted")
        pos = self.canvas.coords(0, 480, y)
        print ("coords updated")

    def move_up2(self, evt):
        PORT = 5006
        IP = "172.25.40.161"
        MESSAGE = "SM:1,u"
        print (MESSAGE)
        SMESSAGE = str.encode(MESSAGE)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock1.bind(('',5007))
        sock1.sendto(SMESSAGE, (IP, PORT))
           
    def move_down2(self, evt):
        PORT = 5006
        IP = "172.25.40.161"
        MESSAGE = "SM:1,d"
        print (MESSAGE)
        SMESSAGE = str.encode(MESSAGE)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock1.bind(('',5007))
        sock1.sendto(SMESSAGE, (IP, PORT))

# Create window and canvas to draw on
tk = Tk()
tk.title("Ping")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='white')
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'black')
paddle2 = Paddle2(canvas, 'black')
ball = Ball(canvas, 'black', 25, paddle, paddle2)
UDP_IP = "0.0.0.0"
UDP_PORT = 55433
 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)
holder = ["1","150","150","250","200","0","0",0]
isLoss = False
toParse = ""
# Animation loop
while isLoss != True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print ("received message:", data)
        toParse = data.decode("utf-8")
        print (toParse)
        holder = toParse.split(",")
        print (holder)
    except:
        pass
    if holder[7] == "1":
        isLoss = True
    paddle.draw(holder[1])
    paddle2.draw(holder[2])
    ball.draw(holder[3],holder[4])
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)



# Game Over
go_label = canvas.create_text(250,200,text="GAME OVER",font=("Helvetica",30))
tk.update()
