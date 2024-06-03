from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests, json

app = Flask(__name__)
CORS(app)

API_KEY = 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'
ORDER_ID_GENERATION_URL = 'https://api.tech.redventures.com.br/orders/generate-id'

broths = [
    {
        "id": "1",
        "imageInactive": "https://tech.redventures.com.br/icons/salt/inactive.svg",
        "imageActive": "https://tech.redventures.com.br/icons/salt/active.svg",
        "name": "Salt",
        "description": "Simple like the seawater, nothing more",
        "price": 10
    }
]

proteins = [
    {
        "id": "1",
        "imageInactive": "https://tech.redventures.com.br/icons/pork/inactive.svg",
        "imageActive": "https://tech.redventures.com.br/icons/pork/active.svg",
        "name": "Chasu",
        "description": "A sliced flavourful pork meat with a selection of season vegetables.",
        "price": 10
    }
]

@app.route('/broths', methods=['GET'])
def get_broths():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "x-api-key header missing"}), 403

    return jsonify(broths), 200

@app.route('/proteins', methods=['GET'])
def get_proteins():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "x-api-key header missing"}), 403

    return jsonify(proteins), 200

@app.route('/orders', methods=['POST'])
def place_order():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "x-api-key header missing"}), 403

    # Verifica o Content-Type da requisição
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        data = request.json
    elif content_type == 'text/plain;charset=UTF-8':
        # Converte o texto em um objeto Python
        data = json.loads(request.data.decode('utf-8'))
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

    broth_id = data.get('brothId')
    protein_id = data.get('proteinId')

    if not broth_id or not protein_id:
        return jsonify({"error": "both brothId and proteinId are required"}), 400

    response = requests.post(ORDER_ID_GENERATION_URL, headers={'x-api-key': API_KEY})

    if response.status_code != 200:
        return jsonify({"error": "could not place order"}), 500

    order_id = response.json().get('orderId')
    order_description = f"{next(b['name'] for b in broths if b['id'] == broth_id)} and {next(p['name'] for p in proteins if p['id'] == protein_id)} Ramen"
    order_image = "https://tech.redventures.com.br/icons/ramen/ramenChasu.png"

    return jsonify({
        "id": order_id,
        "description": order_description,
        "image": order_image
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
