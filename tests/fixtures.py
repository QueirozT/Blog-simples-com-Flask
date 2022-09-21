from config import TestConfig
from pytest import fixture

from app import create_app
from app.models import db, User
    

@fixture(scope='function')
def func_app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()
        db.session.remove()


@fixture(scope='module')
def modul_app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()
        db.session.remove()


@fixture(scope='module')
def testing_client():
    app = create_app(TestConfig)

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def create_user(name):
    user = User(username=name, email=f'{name}@email.com')
    user.set_password('senha')
    return user
