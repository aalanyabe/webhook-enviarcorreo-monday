from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verificar que la solicitud sea JSON
    if request.is_json:
        data = request.get_json()  # Obtener el cuerpo JSON de la solicitud
        
        # Procesar el desafío que envía Monday (si existe)
        if "challenge" in data:
            print(f"Webhook received: {data}")
            # Responder al webhook con el desafío
            response = make_response(jsonify({'challenge': data['challenge']},200))
            response.headers['ngrok-skip-browser-warning'] = 'true'
            return response

            # return jsonify({'challenge': data['challenge']}), 200
        else:
            return jsonify({'error': 'No se encontró el campo challenge'}), 400
    else:
        return jsonify({'error': 'El cuerpo no es JSON o Content-Type incorrecto'}), 415  # 415: Unsupported Media Type

if __name__ == '__main__':
    app.run(port=5000, debug=True)
