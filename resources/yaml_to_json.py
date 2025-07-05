from flask_restful import Resource
from flask import request, jsonify
import yaml

class YamlToJsonConverter(Resource):

    def get(self):
        return "This endpoint only accepts POST requests with a YAML body"

    def post(self):
        try:
            # Get raw YAML data from request body
            yaml_data = request.data.decode('utf-8')

            # Parse YAML to Python dictionary
            parsed_data = yaml.safe_load(yaml_data)

            # Return JSON response
            return jsonify(parsed_data)

        except Exception as e:
            return {"error": str(e)}, 400
