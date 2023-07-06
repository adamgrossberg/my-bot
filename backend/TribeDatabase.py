
from pymongo.mongo_client import MongoClient
from collections.abc import Iterable

class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.db
        self.players = self.db.players
        self.teams = self.db.teams
    
    def insert_player(self, id, name, team):
        self.players.insert_one({
            '_id': id,
            'name': name,
            'points': 0,
            'minutes': 0,
            'team': team
        })
    
    def insert_many_players(self, players: Iterable):
        for player in players:
            self.insert_player(player['id'], player['name'], player['team'])
    
    def delete_player(self, id):
        self.players.delete_one({'_id': id})
    
    def delete_all_players(self):
        self.players.delete_many({})
    
    def inc_player_values(self, id: str, value: str, increment: int):
        self.players.update_one({'_id': id}, {'$inc': {value: increment}})

    def get_all_players(self):
        return self.players.find()