from config import Config
from pytest import fixture

from app import create_app


class TestConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    

@fixture(scope='module')
def app():
    app = create_app(TestConfig)

    with app.app_context():
        app.db.create_all()

        yield app
