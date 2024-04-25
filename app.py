from flask import Flask, request, jsonify
import processor as proc
app = Flask(__name__)

# Lista para almacenar las evaluaciones
evaluaciones = []

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

if __name__ == '__main__':
    app.run(debug=True)