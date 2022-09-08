from flask import Flask

from .blog import bp_blog

def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp_blog)

    return app
