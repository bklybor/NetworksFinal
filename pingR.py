import socket
from pynput import keyboard
from tkinter import *
import random
import time

# Here we are starting a keyboard listener and getting all up or down key presses then sending a 1 or 0 to the server.
def upordown(key): # when pressing up or down
    try: k = key.char # gets the character of key
    except: k = key.name # else get the name of key
    
    if k in ['up', 'down']: # if user presses down or up key


        if k == 'up':     # if user presses the up arrow key, then send a 1 to the server at the specified IP and PORT
   
            PORT = 5006
            IP = "127.0.0.1"
            MESSAGE = "1"

            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))

        if k == 'down':        # if user presses the down arrow key, then send a 0 to the server at the specified IP and PORT
            IP = "127.0.0.1"
            PORT = 5006
            MESSAGE = "0"
    
            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))
    return False

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle, paddle2):
        self.canvas = canvas
        self.paddle = paddle
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.xspeed = random.randrange(-6,6)
        self.yspeed = -1
        self.hit_right = False
        self.hit_left = False
        self.score = 0

    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.yspeed = 3
        if pos[3] >= 400:
            self.yspeed = -3
        if pos[0] <= 0:
            self.xspeed = 3
            self.hit_left = True
        if pos[2] >= 500:
            self.xspeed = -3
            self.hit_right = True
        if self.hit_paddle(pos) == True:
            self.yspeed = -3
            self.xspeed = random.randrange(0,3)
            self.score += 1
        if self.hit_paddle2(pos) == True:
            self.yspeed = -3
            self.xspeed = random.randrange(-3,0)

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    def hit_paddle2(self, pos):
        paddle_pos2 = self.canvas.coords(self.paddle2.id)
        if pos[2] >= paddle_pos2[0] and pos[0] <= paddle_pos2[2]:
            if pos[3] >= paddle_pos2[1] and pos[3] <= paddle_pos2[3]:
                return True
        return False

# Define paddle properties and functions
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) 
        self.yspeed = 0
        self.canvas.move(self.id, 10, 30 )
        self.canvas.bind_all('<KeyPress-Up>', self.move_up)
        self.canvas.bind_all('<KeyPress-Down>', self.move_down)

    def draw(self):
        self.canvas.move(self.id, self.yspeed, 0)
        pos = self.canvas.coords(self.id)

    def move_up(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[1] > 5:
            self.canvas.move(self.id, 0, -20)
            PORT = 5006
            IP = "127.0.0.1"
            MESSAGE = "1"
            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))
            
    def move_down(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[3] < 400:
            self.canvas.move(self.id, 0, 20)
            PORT = 5006
            IP = "127.0.0.1"
            MESSAGE = "0"
            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))

class Paddle2:
    def __init__(self, canvas, color):
       self.canvas = canvas
       self.id = canvas.create_rectangle(0,0, 10, 100, fill=color) 
       self.yspeed = 0
       self.canvas.move(self.id, 480, 30 )
       self.canvas.bind_all('<KeyPress-Up>', self.move_up2)
       self.canvas.bind_all('<KeyPress-Down>', self.move_down2)

    def draw(self):
        self.canvas.move(self.id, self.yspeed, 0)
        pos = self.canvas.coords(self.id)

    def move_up2(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[1] > 15:
            self.canvas.move(self.id, 0, -20)
            PORT = 5006
            IP = "127.0.0.1"
            MESSAGE = "1"
            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))
           
    def move_down2(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[3] < 400:
            self.canvas.move(self.id, 0, 20)
            PORT = 5006
            IP = "127.0.0.1"
            MESSAGE = "0"
            print (MESSAGE)
   
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.sendto(MESSAGE.encode(), (IP, PORT))

# Create window and canvas to draw on
tk = Tk()
tk.title("Ping")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='white')
canvas.pack()
#label = canvas.create_text(210,5, anchor=NW, text="Player 1 Score: ")
tk.update()
paddle = Paddle(canvas, 'black')
paddle2 = Paddle2(canvas, 'black')
ball = Ball(canvas, 'black', 25, paddle, paddle2)

# Animation loop
while ball.hit_right == False and ball.hit_left == False:
    ball.draw()
    paddle2.draw()
   # canvas.itemconfig(label, text="Player 1 Score: " + str(ball.score))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)



# Game Over
go_label = canvas.create_text(250,200,text="GAME OVER",font=("Helvetica",30))
tk.update()


