# import pingR 
import random

# not the player's ip acts as their id in this class
class game(object):
    def __init__(self, player1_id, player2_id, game_id):
        self.player1 = player1_id
        self.player2 = player2_id
        self.id = game_id
        self.player1_y_pos = 150
        self.player1_x_pos = 480
        self.player2_y_pos = 150
        self.player2_x_pos = 10
        self.ball_x_pos = 250
        self.ball_y_pos = 200
        self.box_width = 500
        self.box_height = 400
        self.player1_score = 0
        self.player2_score = 0
        self.r_hit = False
        self.l_hit = False
        self.is_loss = False
        self.ball_size = 10
        self.paddle_width = 10
        self.paddle_length = 100
        self.move_speed = 10

    def move_up(self, player_id):
        if player_id == self.player1:
            self.player1_y_pos = self.player1_y_pos + self.move_speed
        else:
            self.player2_y_pos = self.player2_y_pos + self.move_speed

    def move_down(self, player_id):
        if player_id == self.player1:
            self.player1_y_pos = self.player1_y_pos - self.move_speed
        else:
            self.player2_y_pos = self.player2_y_pos - self.move_speed

    def move_ball(self, x_speed, y_speed):
        self.ball_x_pos = self.ball_x_pos - x_speed
        self.ball_y_pos = self.ball_y_pos - y_speed
        if self.ball_x_pos <=0:
            self.is_loss = True
        elif self.ball_x_pos >= self.box_witdth:
            self.is_loss = True

        if self.ball_y_pos <= 0:
            self.ball_y_pos = self.ball_y_pos + 10


    def is_l_paddle_hit(self):
        if self.ball_x_pos <= (self.player1_x_pos + self.paddle_width):
            if self.ball_y_pos >= self.player1_y_pos - self.ball_size and self.ball_y_pos <= self.player1_y_pos:
                l_hit = True
    
    def is_r_paddle_hit(self):
        toReturn = False
        if self.ball_x_pos >= self.player2_x_pos:
            if self.ball_y_pos >= self.player1_y_pos - self.ball_size and self.ball_y_pos >= self.player1_y_pos:
                r_hit = True



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