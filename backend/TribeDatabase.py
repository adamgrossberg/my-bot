
from pymongo.mongo_client import MongoClient
from collections.abc import Iterable

class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.db
        self.teams = self.db.teams
        self.players = self.db.players
    
    # Player collection methods

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
    
    def inc_player_value(self, query: dict, attr: str, increment: int):
        self.players.update_one(query, {'$inc': {attr: increment}})
    
    def set_player_value(self, query: dict, attr: str, value: int):
        self.players.update_one(query, {'$set': {attr: value}})

    def get_all_players(self):
        return self.players.find()
    
    def get_player_by_id(self, id):
        return self.players.find_one({'_id': id})

    # Team collection methods
    def delete_all_teams(self):
        self.teams.delete_many({})

    def add_player_to_team(self, player_id, team_id):
        self.set_player_value({'_id': player_id}, 'team', team_id)
        self.teams.update_one({'_id': team_id}, {'$inc': {'total_points': self.get_player_by_id(player_id)['points']}})
        self.teams.update_one({'_id': team_id}, {'$inc': {'total_minutes': self.get_player_by_id(player_id)['minutes']}})
        self.teams.update_one({'_id': team_id}, {'$push': {'members': player_id}})

    def insert_team(self, id, name, member_ids):
        total_points = 0
        total_minutes = 0
        for mem_id in member_ids:
            member = self.get_player_by_id(mem_id)
            total_points += member['points']
            total_minutes += member['minutes']
        self.teams.insert_one({
            '_id': id,
            'name': name,
            'total_points': total_points,
            'total_minutes': total_minutes,
            'members': member_ids
        })

    def inc_team_value(self, query: dict, attr: str, increment: int):
        self.teams.update_one(query, {'$inc': {attr: increment}})

    def get_all_teams(self):
        return self.teams.find()