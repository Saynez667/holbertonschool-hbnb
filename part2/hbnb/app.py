from flask import Flask
from flask_restx import Api
from hbnb.presentation.api import api as api_blueprint

app = Flask(__name__)
api = Api(app)

app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
