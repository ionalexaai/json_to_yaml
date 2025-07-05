from flask import Flask
from flask_restful import Api
from resources.json_to_yaml import JsonToYamlConverter

app = Flask(__name__)
api = Api(app)

api.add_resource(JsonToYamlConverter, "/api/json_to_yaml")

@app.route('/')
def welcome():
    """Small converter API collection"""

    return "Small converter API collection"

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=3000, debug=True)