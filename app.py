from flask import Flask
from form_routes import routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(routes,url_prefix = "/api")

if __name__ ==  '__main__':
    app.run(debug=True)