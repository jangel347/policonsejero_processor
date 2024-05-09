class RulesDB:
    def __init__(self, conn):
        self.conn = conn
        self.collection = self.conn.db["rules"]

    def get_all(self):
        # Consulta a la colección "rules"
        rules = self.collection.find({})

        # Conversión de los resultados a JSON
        rules_json = []
        for rule in rules:
            rule["_id"] = str(rule["_id"])
            rules_json.append(rule)

        return rules_json

    def get_rule_by_id(self, rule_id):
        # Conversión del ID a ObjectId
        object_id = ObjectId(rule_id)

        # Consulta a la colección "rules" por ID
        rule = self.collection.find_one({"_id": object_id})

        # Verificación si la regla existe
        if not rule:
            return None

        # Conversión de la regla a JSON
        rule_json = rule

        return rule_json

    def create_rule(self, new_rule):
        # Inserción de la nueva regla en la colección "rules"
        result = self.collection.insert_one(new_rule)

        # Obtención del ID de la nueva regla
        rule_id = result.inserted_id

        # Conversión de la nueva regla a JSON
        new_rule_json = new_rule

        return rule_id, new_rule_json

    def update_rule(self, rule_id, updated_rule):
        # Conversión del ID a ObjectId
        object_id = ObjectId(rule_id)

        # Actualización de la regla en la colección "rules"
        result = self.collection.update_one({"_id": object_id}, {"$set": updated_rule})

        # Verificación si la regla se actualizó correctamente
        if result.modified_count == 0:
            return None

        # Conversión de la regla actualizada a JSON
        updated_rule_json = updated_rule

        return updated_rule_json

    def delete_rule(self, rule_id):
        # Conversión del ID a ObjectId
        object_id = ObjectId(rule_id)

        # Eliminación de la regla de la colección "rules"
        result = self.collection.delete_one({"_id": object_id})

        # Verificación si la regla se eliminó correctamente
        if result.deleted_count == 0:
            return False

        return True