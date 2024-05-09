from pymongo import MongoClient
class MongoConnection:
    def __init__(self):
        # Conexión a la base de datos MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["poli_consejero"]