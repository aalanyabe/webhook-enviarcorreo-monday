# from flask import Flask, request, abort

# app = Flask(__name__)

# @app.route('/webhook', methods = ['POST'])
# def webhook():
#     if request.method == 'POST':
#         print(request.json)
#         return request.json, 200
#     else:
#         abort(400)

# if __name__ == '__main__':
#     app.run()


# from flask import Flask, request, abort, jsonify

# app = Flask(__name__)

# @app.route('/webhook', methods = ['POST'])
# def webhook():

#     if request.method == 'POST':
#         data = request.json
#         if "challenge" in data:
#             print(f"Webhook received: {data}")
#             # Responder al webhook con el desafío
#             response = {
#                 "challenge": data["challenge"]
#             }
#             return jsonify(response),200
#         else:
#             return jsonify({"error": "no se encontró el campo desafio"}), 400
        
#     else:
#         abort(400)

# if __name__ == '__main__':
#     app.run()


# from flask import Flask, request, abort, jsonify

# app = Flask(__name__)

# @app.route('/webhook', methods = ['POST'])
# def webhook():

#     if request.method == 'POST':
#         data = request.json
#         if "challenge" in data:
#             print(f"Webhook received: {data}")
#             # Responder al webhook con el desafío
#             response = {
#                 "challenge": data["challenge"]
#             }
#             return jsonify(response),200
#         else:
#             print(data)
#             return jsonify(request.json),200
#             # return jsonify({"error": "no se encontró el campo desafio"}), 400
        
#     else:
#         abort(400)

# if __name__ == '__main__':
#     app.run()


from flask import Flask, request, abort, jsonify,json, requests

app = Flask(__name__)


def update_column_value(item_id,board,column_id,value):
    url = "https://api.monday.com/v2"
    
    # crea el payload para la mutacion
    payload = json.dumps({
    "query": "mutation {change_column_value(item_id: 1234567890, board_id: 1122334455, column_id: \"email\", value: \"{\\\"text\\\":\\\"test@gmail.com\\\",\\\"email\\\":\\\"test@gmail.com\\\"}\") {id}}" 
})
    
    headers = {
  'Authorization': 'RELEVANT_API_KEY',
  'Content-Type': 'application/json',
  'API-version': '2023-10'
}
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

@app.route('/webhook', methods = ['POST'])

def webhook():

    if request.method == 'POST':
        data = request.json
        if "challenge" in data:
            print(f"Webhook received: {data}")
            # Responder al webhook con el desafío
            response = {
                "challenge": data["challenge"]
            }
            return jsonify(response),200
        else:
            # print(data)
            # return jsonify(request.json),200
            
            print(f"Received data: {data}")
            # Aquí puedes extraer el ID del ítem, el ID del tablero y otros valores necesarios del payload
            item_id = data.get("item_id")  # Asumiendo que el ID del ítem se envía en el payload
            board_id = data.get("board_id")  # Asumiendo que el ID del tablero se envía en el payload
            column_id = "email"  # O cualquier ID de columna que desees actualizar
            new_value = json.dumps({"text": "test@gmail.com", "email": "test@gmail.com"})  # El nuevo valor que deseas establecer
            
            # Llama a la función para actualizar la columna
            update_response = update_column_value(item_id, board_id, column_id, new_value)
            print(f"Update response: {update_response}")

            return jsonify(update_response), 200
            
        
    else:
        abort(400)

if __name__ == '__main__':
    app.run()


