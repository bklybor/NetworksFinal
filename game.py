# import pingR 

# not the player's ip acts as their id in this class
class game(object):
    def __init__(self, player1_id, player2_id, game_id):
        self.player1 = player1_id
        self.player2 = player2_id
        self.id = game_id
        self.player1_pos = 150
        self.player2_pos = 150
        self.ball_x_pos = 250
        self.ball_y_pos = 200
        self.box_width = 500
        self.box_height = 400
        self.player1_score = 0
        self.player2_score = 0
        self.is_loss = False

    def move_up(self, player_id):
        if player_id == self.player1:
            self.player1_pos = self.player1_pos + 1
        else:
            self.player2_pos = self.player2_pos + 1

    def move_down(self, player_id):
        if player_id == self.player1:
            self.player1_pos = self.player1_pos - 1
        else:
            self.player2_pos = self.player2_pos - 1