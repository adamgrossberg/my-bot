class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.workout_points = 0
        self.throwing_minutes = 0

    def get_database_document(self):
        return {
            "_id": self.id,
            "name": self.name,
            "points": 0,
            "minutes": 0,
            "team": None
        }
