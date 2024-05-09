class TagsDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["tags"]

    def get_all(self):
        # Consulta a la colección "rules"
        rules = self.collection.find({})
        # Conversión de los resultados a JSON
        rules_json = []
        for rule in rules:
            rule["_id"] = str(rule["_id"])
            rules_json.append(rule)

        return rules_json