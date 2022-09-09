from flask import Flask
from config import Config
from flask_babel import Babel
from flask_migrate import Migrate

from .blog import bp_blog
from .models import config as config_db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    babel = Babel(app)

    config_db(app)
    migrate = Migrate(app, app.db)

    app.register_blueprint(bp_blog)

    return app
