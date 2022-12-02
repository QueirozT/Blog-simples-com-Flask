from config import TestConfig
from pytest import fixture

from app import create_app


@fixture(scope='function')
def app():
    app = create_app(TestConfig)

    with app.app_context():
        app.db.create_all()

        yield app

        app.db.drop_all()
        app.db.session.remove()


@fixture(scope='function')
def client():
    app = create_app(TestConfig)
    
    app.test_request_context().push()
    app.db.create_all()

    yield app.test_client()

    app.db.drop_all()
    app.db.session.remove()
