class RegulationsDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["regulations"]

    def get_all(self):
        # Consulta a la colección "regulations"
        regulations = self.collection.find({})
        # Conversión de los resultados a JSON
        regulations_json = []
        for regulation in regulations:
            regulation["_id"] = str(regulation["_id"])
            regulations_json.append(regulation)

        return regulations_json