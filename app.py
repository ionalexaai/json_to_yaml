from flask import Flask
from flask_restful import Api
from resources.json_to_yaml import JsonToYamlConverter
from resources.yaml_to_json import YamlToJsonConverter

app = Flask(__name__)
api = Api(app)

api.add_resource(JsonToYamlConverter, "/api/json_to_yaml")
api.add_resource(YamlToJsonConverter, "/api/yaml_to_json")

@app.route('/')
def welcome():
    """Small converter API collection"""

    return "Small converter API collection"

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)