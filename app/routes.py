from resources.json_to_yaml import JsonToYamlConverter
from resources.yaml_to_json import YamlToJsonConverter

def register_resources(api):
    """Register API resources with Flask-RESTful"""
    api.add_resource(JsonToYamlConverter, '/api/json_to_yaml')
    api.add_resource(YamlToJsonConverter, '/api/yaml_to_json')
