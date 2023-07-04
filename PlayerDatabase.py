
from pymongo.mongo_client import MongoClient
from collections.abc import Iterable

class PlayerDatabase:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.db
        self.players = self.db.players
        self.teams = self.db.teams
    
    def insert_one_player(self, id, name, team):
        self.players.insert_one({
            '_id': id,
            'name': name,
            'points': 0,
            'minutes': 0,
            'team': team
        })
    
    def insert_many_players(self, players: Iterable):
        for player in players:
            self.insert_one_player(player['id'], player['name'], player['team'])
    
    def print_players(self):
        for player in self.players.find():
            print(player)