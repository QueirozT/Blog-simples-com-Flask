from datetime import datetime, timedelta

from app.models import Post, User


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


def test_de_follow_deve_retornar_vazio(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

    app.db.session.add_all([u1, u2])
    app.db.session.commit()

    assert u1.followed.all() == []
    assert u1.followers.all() == []
    assert u2.followed.all() == []
    assert u2.followers.all() == []


def test_de_followed_deve_retornar_u2(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

    app.db.session.add_all([u1, u2])

    u1.follow(u2)

    app.db.session.commit()

    assert u1.followed.all() == [u2]


def test_de_follower_deve_retornar_u1(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

    app.db.session.add_all([u1, u2])

    u1.follow(u2)

    app.db.session.commit()

    assert u2.followers.all() == [u1]


def test_de_follow_deve_retornar_username_correspondente(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

    app.db.session.add_all([u1, u2])

    u1.follow(u2)

    app.db.session.commit()
    
    assert u1.followed.first().username == 'usuario2'
    assert u2.followers.first().username == 'usuario1'


def test_de_follow_cont_deve_retornar_zero(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

    app.db.session.add_all([u1, u2])

    u1.follow(u2)

    app.db.session.commit()

    assert u2.followed.count() == 0
    assert u1.followers.count() == 0


def test_de_posts_deve_retornar_post_de_u1_e_u2(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

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

    app.db.session.add_all([u1, u2, p1, p2])
    app.db.session.commit()

    assert Post.query.filter_by(user_id=u1.id).first() == p1
    assert Post.query.filter_by(user_id=u2.id).first() == p2


def test_de_followed_posts_deve_retornar_dois_posts(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

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

    app.db.session.add_all([u1, u2, p1, p2])

    u1.follow(u2)

    app.db.session.commit()

    assert u1.followed_posts().count() == 2


def test_de_followed_posts_deve_retornar_um_post_do_u2(app):
    u1 = create_user('usuario1')
    u2 = create_user('usuario2')

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

    app.db.session.add_all([u1, u2, p1, p2])

    u1.follow(u2)

    app.db.session.commit()

    assert u2.followed_posts().count() == 1
    assert u2.followed_posts().first() == p2
