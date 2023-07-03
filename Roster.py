import Player

class Roster:
    def __init__(self):
        self.players = []
    
    def add_player(self, player: Player):
        self.players.append(player)