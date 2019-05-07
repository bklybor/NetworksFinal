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
        
        self.player1_score = 0
        self.player2_score = 0
        self.r_hit = False
        self.l_hit = False
        self.is_loss = False

        self.move_speed = 10
        
        self.ball = Ball((self.player1_x_pos,self.player1_y_pos), (self.player2_x_pos,self.player2_y_pos))

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

    # returns a tuple containing the ball's x and y position
    def move_ball(self):
        self.ball.draw()
        self.ball_x_pos = self.ball.ball_x_pos
        self.ball_y_pos = self.ball.ball_y_pos
        




class Ball:
    def __init__(self, p1_pos, p2_pos):

        self.xspeed = 10
        self.yspeed = -5
        self.hit_right = False
        self.hit_left = False
        self.score = 0
        self.ball_x_pos = 250
        self.ball_y_pos = 200
        self.box_width = 500
        self.box_height = 400
        self.ball_size = 10
        self.paddle_width = 10
        self.paddle_length = 100

        self.speed = 10

        self.p1_x_pos, self.p1_y_pos = p1_pos
        self.p2_x_pos, self.p2_y_pos = p2_pos
        # self.move_speed = random.randrange(-6,6)

    def draw(self):

        if self.ball_y_pos <= -80:
            self.yspeed = self.speed
        if self.ball_y_pos >= self.box_height - 100:
            self.yspeed = -(self.speed)
        if self.ball_x_pos <= 0:
            self.xspeed = self.speed
            self.hit_left = True
        if self.ball_x_pos >= self.box_width:
            self.xspeed = -(self.speed)
            self.hit_right = True
        if self.hit_paddle() == True:
            self.yspeed = -(self.speed)
            self.xspeed = random.randrange(0,10)
        if self.hit_paddle2() == True:
            self.yspeed = -3
            self.xspeed = random.randrange(-10,0)

        self.ball_x_pos = self.ball_x_pos + self.xspeed
        self.ball_y_pos = self.ball_y_pos + self.yspeed

    def hit_paddle(self):
        if self.ball_x_pos <= self.p1_x_pos and self.ball_x_pos + self.ball_size >= self.p1_x_pos + self.paddle_width:
            if self.ball_y_pos + self.ball_size >= self.p1_y_pos and self.ball_y_pos <= self.p1_y_pos + self.paddle_length:
                return True
        return False
    
    def hit_paddle2(self):
        if self.ball_x_pos <= self.p2_x_pos and self.ball_x_pos + self.ball_size >= self.p2_x_pos:
            if self.ball_y_pos + self.ball_size >= self.p2_y_pos and self.ball_y_pos <= self.p2_y_pos + self.paddle_length:
                return True
        return False