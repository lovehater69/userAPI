from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

mongo_db = MongoDB("mongodb://localhost:27017/", "user_database")
