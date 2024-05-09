import spacy
from logic.situation_processor import SituationProcessor
from database.rules_db import RulesDB  # Importar la clase RulesDB
from logic.clasification import Classifier
from flask import Flask, request, jsonify
import processor as proc
app = Flask(__name__)

PATH ='./dataset/dataset.csv'

rules_db = RulesDB()
RULES_LIST = rules_db.get_all_rules()

NLP = spacy.load("es_core_news_sm")

@app.route("/rules", methods=["GET"])
def get_all_rules():
    rules_json = rules_db.get_all_rules()
    return jsonify({"rules": rules_json})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    print(data)
    if not data:
        return jsonify({'error': 'No se han proporcionado datos'}), 400
    #tag prediction
    classifier = Classifier(PATH)
    predict = classifier.generate_predict([data["situation"]])
    # print(f'PREDICT {predict}')

    # situation process
    processor = SituationProcessor(NLP)
    processor.load_situation('Créditos académicos')
    processor.load_rules(RULES_LIST)
    rules = processor.get_rules()


    return jsonify({
        'response': 'Respuesta de prueba',
        'rules': rules,
        'tags':[predict]
        }), 201


if __name__ == '__main__':
    app.run(debug=True)