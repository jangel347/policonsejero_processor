class RulesDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["rules"]

    def get_all(self):
        rules = self.collection.find({})

        rules_json = []
        for rule in rules:
            rule["_id"] = str(rule["_id"])
            rules_json.append(rule)

        return rules_json
    
    def get_rules_by(self, by):
        rules = self.collection.find(by)
        rules_json = []
        for rule in rules:
            rule["_id"] = str(rule["_id"])
            rules_json.append(rule)

        return rules_json
    


    def get_rule_by_id(self, rule_id):
        object_id = ObjectId(rule_id)

        rule = self.collection.find_one({"_id": object_id})

        if not rule:
            return None

        rule_json = rule

        return rule_json

    def create_rule(self, new_rule):
        result = self.collection.insert_one(new_rule)

        rule_id = result.inserted_id

        new_rule_json = new_rule

        return rule_id, new_rule_json

    def update_rule(self, rule_id, updated_rule):
        object_id = ObjectId(rule_id)

        result = self.collection.update_one({"_id": object_id}, {"$set": updated_rule})

        if result.modified_count == 0:
            return None

        updated_rule_json = updated_rule

        return updated_rule_json

    def delete_rule(self, rule_id):
        object_id = ObjectId(rule_id)

        result = self.collection.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            return False

        return True