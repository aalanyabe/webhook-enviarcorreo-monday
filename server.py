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


from flask import Flask, request, abort, jsonify

app = Flask(__name__)

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
            print(data)
            return jsonify(request.json),200
            # return jsonify({"error": "no se encontró el campo desafio"}), 400
        
    else:
        abort(400)

if __name__ == '__main__':
    app.run()


