
from pymongo.mongo_client import MongoClient

import Player

class PlayerDatabase:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.db
        self.players = self.db.players
    
    def insert_player(self, player: Player):
        self.players.insert_one(player.get_database_document())
    
    def print_players(self):
        for player in self.players.find():
            print(player)