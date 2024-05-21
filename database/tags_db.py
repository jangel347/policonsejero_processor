class TagsDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["tags"]

    def get_all(self):
        # Consulta a la colección "tags"
        tags = self.collection.find({})
        # Conversión de los resultados a JSON
        tags_json = []
        for tag in tags:
            tag["_id"] = str(tag["_id"])
            tags_json.append(tag)

        return tags_json