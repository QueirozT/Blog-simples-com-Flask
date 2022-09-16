import pytest
from datetime import datetime, timedelta

from app import create_app
from app.models import User, Post


@pytest.fixture
def app():    
    app = create_app()
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    app_ctx = app.app_context()
    app_ctx.push()
    
    app.db.create_all()

    return app


def create_user(name):
    user = User(username=name, email=f'{name}@email.com')
    user.set_password('senha')
    return user


def test_password_hash_deve_retornar_true():
    user = create_user('usuario')
    assert user.check_password('senha') == True


def test_password_hash_deve_retornar_false():
    user = create_user('usuario')
    assert user.check_password('senha2') == False


def test_avatar_deve_retornar_url_do_gravatar():
    user = create_user('usuario')
    assert user.avatar(128) == ('https://www.gravatar.com/avatar/38ae40c822b47147d36b838bbc2e774d?d=identicon&s=128')


def test_de_followed_deve_retornar_vazio(app):
    u1 = create_user('usuario1')

    app.db.session.add(u1)
    app.db.session.commit()

    assert u1.followed.all() == []


def test_de_follower_deve_retornar_vazio(app):
    u2 = create_user('usuario2')

    app.db.session.add(u2)
    app.db.session.commit()

    assert u2.followers.all() == []


def test_de_followed_deve_retornar_u2(app):
    u1 = User.query.filter_by(username='usuario1').first()
    u2 = User.query.filter_by(username='usuario2').first()
    
    u1.follow(u2)
    app.db.session.commit()

    assert u1.followed.all() == [u2]


def test_de_follower_deve_retornar_u1(app):
    u1 = User.query.filter_by(username='usuario1').first()
    u2 = User.query.filter_by(username='usuario2').first()

    assert u2.followers.all() == [u1]


def test_de_followed_username_deve_retornar_usuario2(app):
    u1 = User.query.filter_by(username='usuario1').first()
    
    assert u1.followed.first().username == 'usuario2'


def test_de_follower_deve_retornar_usuario1(app):
    u2 = User.query.filter_by(username='usuario2').first()

    assert u2.followers.first().username == 'usuario1'


def test_de_followed_deve_retornar_zero(app):
    u1 = User.query.filter_by(username='usuario1').first()
    u2 = User.query.filter_by(username='usuario2').first()

    u1.unfollow(u2)

    assert u1.followed.count() == 0


def test_de_followed_posts_deve_retornar_dois_posts(app):
    u1 = User.query.filter_by(username='usuario1').first()
    u2 = User.query.filter_by(username='usuario2').first()

    now = datetime.utcnow()

    p1 = Post(
        body='Post de Usuario1', 
        author=u1, 
        timestamp=now + timedelta(seconds=2)
    )

    p2 = Post(
        body='Post de Usuario2',
        author=u2,
        timestamp=now + timedelta(seconds=4)
    )

    app.db.session.add_all([p1, p2])
    app.db.session.commit()

    u1.follow(u2)
    app.db.session.commit()

    assert u1.followed_posts().count() == 2


def test_de_follow_posts_deve_retornar_post_de_u1_e_u2(app):    
    u1 = User.query.filter_by(username='usuario1').first()
    u2 = User.query.filter_by(username='usuario2').first()

    p1 = Post.query.filter_by(user_id=u1.id).first()
    p2 = Post.query.filter_by(user_id=u2.id).first()

    assert Post.query.all() == [p1, p2]


def test_de_follow_posts_deve_retornar_zero_posts(app):
    u3 = create_user('usuario3')

    assert u3.followed_posts().count() == 0
