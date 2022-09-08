from flask import Flask
from flask_babel import Babel
from config import Config

from .blog import bp_blog

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    babel = Babel(app)

    app.register_blueprint(bp_blog)

    return app
