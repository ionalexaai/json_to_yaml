from flask_restful import Resource
from flask import request, make_response
import yaml

class JsonToYamlConverter(Resource):

    def get(self):
        return "This endpoint only accepts POST requests with a JSON body"

    def post(self):
        try:
            # Get JSON data from the request body
            json_data = request.get_json(force=True)

            # Convert JSON to YAML
            yaml_data = yaml.dump(json_data, sort_keys=False)

            # Return YAML with plain text response
            response = make_response(yaml_data, 200)
            response.mimetype = "text/plain"
            return response

        except Exception as e:
            return {"error": str(e)}, 400
