from flask import Flask
from flask_restful import Api
from app.routes import register_resources

def create_app():
    """Application factory for creating Flask app instances"""
    app = Flask(__name__)
    api = Api(app)

    register_resources(api)

    @app.route('/')
    def index():
        return "Small converter API collection"

    return app
