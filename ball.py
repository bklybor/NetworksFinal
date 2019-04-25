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
