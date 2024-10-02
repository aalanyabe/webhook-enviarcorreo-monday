from flask import Flask, jsonify,abort,request
from dotenv import load_dotenv
import os
import requests
import json

app = Flask(__name__)

load_dotenv()

# ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE4MDk4NjgyNSwiYWFpIjoxMSwidWlkIjozMDQ2ODAyNywiaWFkIjoiMjAyMi0wOS0xNFQyMjoxODoxOS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTE3MTIwMjYsInJnbiI6InVzZTEifQ.TU91f8lcu2mspQDy-BHlOuXzgZt3RQTuGMOp6GDh4N8"
# base_store_board_id = 6750853855
# target_board_email_column_id= 'correo_electr_nico__1'
# base_borad_email_column_id = 'correo_electr_nico__1'
# foreign_email_colum_id_target_board = 'texto4__1'

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
base_store_board_id = os.getenv("BASE_STORE_BOARD_ID")
target_board_email_column_id= os.getenv("TARGET_BOARD_EMAIL_COLUMN_ID")
base_board_email_column_id = os.getenv("BASE_BOARD_EMAIL_COLUMN_ID")
foreign_email_colum_id_target_board = os.getenv("FOREIGN_EMAIL_COLUMN_ID_TARGET_BOARD")



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

def get_store_email(board_id,store_name):
    urlAPI = "https://api.monday.com/v2"
    payload = json.dumps({
        "query": f'{{boards(ids: {board_id}) {{name id description items_page (limit:500){{ cursor items{{ name column_values{{ id text type ... on DateValue {{ time date }}}}}}}}}}}}'
    })
    headers = {
    'Authorization': ACCESS_TOKEN,
    'Content-Type': 'application/json',
    'API-version': '2023-10'
    }
    response = requests.request("POST", urlAPI, headers=headers, data=payload)

    data=response.json()
    print(f'data es: {data}')

    for item in data['data']['boards'][0]['items_page']['items']:
        if item['name'] == store_name:
            for column in item['column_values']:
                if column['id'] == base_board_email_column_id:
                    return f"correo@gmail.com {column['text']}"


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
            store_name = data.get("event",()).get("columnValues",{}).get(foreign_email_colum_id_target_board,{}).get("chosenValues",[])[0].get("name")

            new_value = get_store_email(base_store_board_id,store_name)
            
            # # Llama a la función para actualizar la columna
            update_response = update_email_column_value(item_id, board_id, target_board_email_column_id, new_value)
            print(f"Update response: {update_response}")

            return jsonify(update_response), 200
                
    else:
        abort(400)

if __name__ == '__main__':
    app.run()


