from flask import Flask
from .routes import task_bp

def create_app():
    app = Flask(_name_)
    app.register_blueprint(task_bp)
    return app