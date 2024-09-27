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


from flask import Flask, jsonify,abort,request
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE4MDk4NjgyNSwiYWFpIjoxMSwidWlkIjozMDQ2ODAyNywiaWFkIjoiMjAyMi0wOS0xNFQyMjoxODoxOS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTE3MTIwMjYsInJnbiI6InVzZTEifQ.TU91f8lcu2mspQDy-BHlOuXzgZt3RQTuGMOp6GDh4N8"

# item_id = 5794326742
# board_id = 5794268071
column_id= 'correo_electr_nico__1'
new_value = 'aa@gmial.com nuevocorreo'

def update_email_column_value(item_id,board_id,column_id,new_value):
    url = "https://api.monday.com/v2?="
    payload = json.dumps({"query": f'mutation {{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "{column_id}", value: "{new_value}") {{ id }} }}'})

    headers = {
    'Authorization': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'API-version': '2023-10'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


#  Ruta que ejecuta la función cuando se hace una solicitud GET
# @app.route('/update-email', methods=['GET'])
# def update_email_route():
#     result = update_email_column_value()
#     return jsonify({"status": "Email updated", "result": result})


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
            print(f"Received data: {data}")
            # return jsonify(request.json),200
        
            # Aquí puedes extraer el ID del ítem, el ID del tablero y otros valores necesarios del payload
            item_id = data.get("event",()).get("pulseId")
            board_id = data.get("event",()).get("boardId")
            column_id = data.get("event",()).get("columnValues").get(f'{column_id}') 
            new_value = new_value
            
            # # Llama a la función para actualizar la columna
            update_response = update_email_column_value(item_id, board_id, column_id, new_value)
            print(f"Update response: {update_response}")

            return jsonify(update_response), 200
            
        
    else:
        abort(400)

if __name__ == '__main__':
    app.run()


