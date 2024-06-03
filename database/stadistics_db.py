class StadisticsDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["stadistics"]

    def get_all(self):
        stadistics = self.collection.find({})

        stadistics_json = []
        for stadistic in stadistics:
            stadistic["_id"] = str(stadistic["_id"])
            stadistics_json.append(stadistic)

        return stadistics_json
    
    def get_stadistics_by(self, by):
        stadistics = self.collection.find(by)
        stadistics_json = []
        for stadistic in stadistics:
            stadistic["_id"] = str(stadistic["_id"])
            stadistics_json.append(stadistic)

        return stadistics_json
    


    def get_stadistic_by_id(self, stadistic_id):
        object_id = ObjectId(stadistic_id)

        stadistic = self.collection.find_one({"_id": object_id})

        if not stadistic:
            return None

        stadistic_json = stadistic

        return stadistic_json

    def create_stadistic(self, new_stadistic):
        result = self.collection.insert_one(new_stadistic)

        stadistic_id = result.inserted_id

        new_stadistic_json = new_stadistic

        return stadistic_id, new_stadistic_json

    def update_stadistic(self, stadistic_id, updated_stadistic):
        object_id = ObjectId(stadistic_id)

        result = self.collection.update_one({"_id": object_id}, {"$set": updated_stadistic})

        if result.modified_count == 0:
            return None

        updated_stadistic_json = updated_stadistic

        return updated_stadistic_json

    def delete_stadistic(self, stadistic_id):
        object_id = ObjectId(stadistic_id)

        result = self.collection.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            return False

        return True