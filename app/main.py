from flask import Flask
from app.extensions import mongo
from app.blueprints import register_blueprints
import os
from app.config.env import ENV

def create_app() -> Flask:


    # Static files
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    # Create Flask application
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )

    # Configuration
    app.config["SECRET_KEY"] = ENV["SECRET_KEY"]
    app.config["MONGO_URI"] = ENV["MONGO_URI"]

    # Database Connection
    mongo.init_app(app)

    # Register blueprints (routers)
    register_blueprints(app)
    return app


app = create_app()