from flask import Flask, request, jsonify
import processor as proc
app = Flask(__name__)

# Lista para almacenar las evaluaciones
evaluaciones = []

@app.route("/rules", methods=["GET"])
def get_all_rules():
    rules_json = rules_db.get_all_rules()
    return jsonify({"rules": rules_json})

# Definir el endpoint POST /evaluation
@app.route('/evaluation', methods=['POST'])
def add_evaluation():
    data = request.json  # Obtener los datos enviados en formato JSON
    # print(data)
    if not data:
        return jsonify({'error': 'No se han proporcionado datos'}), 400

    reglas, tags = proc.buscar_reglas(data["situation"],data["rules"])
    # Añadir la evaluación a la lista
    return jsonify({
        'response': 'Respuesta de prueba',
        'rules': reglas,
        'tags':tags
        }), 201

import spacy
from logic.situation_processor import SituationProcessor
from database.rules_db import RulesDB  # Importar la clase RulesDB

# ... (resto del código de la API)

# Inicialización de la clase RulesDB
rules_db = RulesDB()

nlp = spacy.load("es_core_news_sm")

processor = SituationProcessor(nlp)
processor.load_situation('Créditos académicos')
processor.load_rules(rules_db.get_all_rules())

rules = processor.get_rules()


for rule in rules:
    print(rule['name'])
    print(rule)
print(f"Reglas encontradas: {len(rules)}")

if __name__ == '__main__':
    app.run(debug=True)