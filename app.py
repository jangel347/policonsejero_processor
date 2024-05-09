import spacy
from logic.situation_processor import SituationProcessor
from database.connection import MongoConnection 
from database.rules_db import RulesDB 
from database.tags_db import TagsDB 
from logic.clasification import Classifier
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

PATH ='./dataset/dataset.csv'

conn = MongoConnection()
rules_db = RulesDB(conn)
tags_db = TagsDB(conn)
RULES_LIST = rules_db.get_all()
TAGS_LIST = tags_db.get_all()

NLP = spacy.load("es_core_news_sm")

@app.route("/rules", methods=["GET"])
@cross_origin()
def get_all_rules():
    rules_json = rules_db.get_all_rules()
    return jsonify({"rules": rules_json})

@app.route('/evaluate', methods=['POST'])
@cross_origin()
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
    processor = SituationProcessor(NLP,RULES_LIST,TAGS_LIST)
    processor.load_situation(data["situation"])
    processor.load_predict(predict)
    processor.debug_on()
    rules = processor.get_rules()
    response = processor.get_response()


    return jsonify({
        'response': response,
        'rules': rules,
        'tags':[predict]
        }), 201


if __name__ == '__main__':
    app.run(debug=True)