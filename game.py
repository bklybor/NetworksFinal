# import pingR 

# not the player's ip acts as their id in this class
class game(object):
    def __init__(self, player1_id, player2_id, game_id):
        self.player1 = player1_id
        self.player2 = player2_id
        self.id = game_id
        self.player1_pos = 0
        self.player2_pos = 0
        self.ball_pos = 0
        self.box_width = 400
        self.box_height = 400

    def move_up(player_id):
        if player_id == player1:
            player1_pos = player1_pos + 1
        else:
            player2_pos = player2_pos + 1

    def move_down(player_id):
        if player_id == player1:
            player1_pos = player1_pos + 1
        else:
            player2_pos = player2_pos + 1