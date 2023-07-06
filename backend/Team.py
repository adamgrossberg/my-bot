class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.total_points = 0
        self.total_minutes = 0
        self.member_ids = []
    
    def get_database_document(self):
        return {
            "_id": self.id,
            "name": self.name,
            "total_points": self.total_points,
            "total_minutes": self.total_minutes,
            "members": self.member_ids
        }