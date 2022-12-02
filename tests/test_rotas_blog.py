from flask import url_for
from flask_login import login_user

from app.models import db, User, Post, Reply


def test_rota_index_deve_retornar_todos_os_posts(client):
    response_sem_posts = client.get(url_for('blog.index'))

    user = User(username='xpto', email='xpto@email.com')
    post = Post(title='todo', body='list todo', user_id=1)
    db.session.add_all([user, post])
    db.session.commit()
    login_user(user)
    response_com_posts = client.get(url_for('blog.index'))

    esperado_sem_posts = "Nenhuma postagem encontrada!"
    esperado_com_posts = "/post_detalhes/xpto/1"

    assert response_sem_posts.status_code == 200
    assert esperado_sem_posts in response_sem_posts.text

    assert response_com_posts.status_code == 200
    assert esperado_com_posts in response_com_posts.text


def test_rota_destaques_deve_redirecionar_para_o_login_quando_nao_autenticado(client):
    response = client.get(url_for('blog.destaques'))

    esperado = 'You should be redirected automatically to the target URL: <a href="/auth/login?next=%2Fdestaques">'

    assert response.status_code == 302
    assert esperado in response.text


def test_rota_destaques_deve_retornar_os_posts_dos_seguidores_quando_autenticado(client):
    user = User(username='xpto', email='xpto@email.com')
    login_user(user)
    response_sem_posts = client.get(url_for('blog.destaques'))

    post = Post(title='todo', body='list todo', user_id=1)
    db.session.add_all([user, post])
    db.session.commit()
    response_com_posts = client.get(url_for('blog.destaques'))

    assert response_sem_posts.status_code == 200
    assert "Nenhuma postagem encontrada!" in response_sem_posts.text
    assert "/post_detalhes/xpto/1" not in response_sem_posts.text

    assert response_com_posts.status_code == 200
    assert "/post_detalhes/xpto/1" in response_com_posts.text
    assert "Nenhuma postagem encontrada!" not in response_com_posts.text


def test_rota_post_detalhes_deve_retornar_os_detalhes_e_respostas_do_post(client):
    user_post = User(username='xpto', email='xpto@email.com')
    user_reply = User(username='todo', email='todo@email.com')
    post = Post(
        title='postagem', body='uma postagem', author=user_post
    )
    db.session.add_all([user_post, user_reply, post])
    db.session.commit()

    response_sem_reply = client.get(url_for(
        'blog.post_detalhes', username=user_post.username, post_id=post.id
    ))
    
    reply = Reply(
        body='uma resposta', author=user_reply, answered=post
    )
    db.session.add(reply)
    db.session.commit()

    response_com_reply  = client.get(url_for(
        'blog.post_detalhes', username=user_post.username, post_id=post.id
    ))

    assert response_sem_reply.status_code == 200
    assert 'uma postagem' in response_sem_reply.text
    assert 'uma resposta' not in response_sem_reply.text

    assert response_com_reply.status_code == 200
    assert 'uma postagem' in response_sem_reply.text
    assert 'uma resposta' in response_com_reply.text
    assert post.replies.count() == 1
    assert user_reply.replies.count() == 1


def test_rota_create_reply_deve_redirecionar_para_login_quando_nao_autenticado(client):
    user = User(username='xpto', email='xpto@email.com')
    post = Post(
        title='postagem', body='uma postagem', user_id=user.id
    )
    db.session.add_all([user, post])
    db.session.commit()

    form = dict(pagedown='uma resposta')

    response = client.post(url_for(
        'blog.create_reply', username=user.username, post_id=post.id
    ), data=form)

    esperado = 'You should be redirected automatically to the target URL: <a href="/auth/login">/auth/login</a>'

    assert response.status_code == 302
    assert esperado in response.text


def test_rota_create_reply_deve_criar_um_reply_quando_autenticado(client):
    user_post = User(username='xpto', email='xpto@email.com')
    user_reply = User(username='todo', email='todo@email.com')
    post = Post(
        title='postagem', body='uma postagem', user_id=user_post.id
    )
    db.session.add_all([user_post, user_reply, post])
    db.session.commit()

    form = dict(pagedown='uma resposta')

    login_user(user_reply)

    response = client.post(url_for(
        'blog.create_reply', username=user_post.username, post_id=post.id
    ), data=form)

    esperado = 'You should be redirected automatically to the target URL: <a href="/post_detalhes/xpto/1">'

    assert response.status_code == 302
    assert esperado in response.text
    assert user_reply.replies.count() == 1


def test_rota_create_post_deve_criar_um_post_e_redirecionar_para_index_quando_autenticado(client):
    user = User(username='xpto', email='xpto@email.com')
    db.session.add(user)
    db.session.commit()
    login_user(user)

    form = dict(title='Titulo', pagedown='Corpo da mensagem')

    response = client.post(url_for('blog.create_post'), data=form)

    esperado = 'You should be redirected automatically to the target URL: <a href="/index">/index</a>'

    assert response.status_code == 302
    assert esperado in response.text
    assert user.posts.count() == 1


def test_rota_user_deve_retornar_os_dados_do_usuario_quando_encontrado(client):
    user = User(username='xpto', email='xpto@email.com')
    db.session.add(user)
    db.session.commit()

    response = client.get(
        url_for('blog.user', username=user.username)
    )

    esperado = 'https://www.gravatar.com/avatar/56dae58a162acfe2bd37dc031cb46f35?d=identicon&amp;s=140'

    assert response.status_code == 200
    assert esperado in response.text
    assert '<h1>xpto</h1>' in response.text


def test_rota_edit_profile_deve_retornar_302_quando_atualizar_um_perfil_autenticado(client):
    user = User(username='xpto', email='xpto@email.com')
    db.session.add(user)
    db.session.commit()
    login_user(user)

    form = dict(
        username='novo',
        email='novo@email.com',
        pagedown='uma descrição'
    )

    response = client.post(url_for('blog.edit_profile'), data=form)

    esperado = 'You should be redirected automatically to the target URL: <a href="/edit_profile">/edit_profile</a>'

    assert response.status_code == 302
    assert esperado in response.text


def test_rota_user_popup_deve_retornar_uma_miniatura_do_perfil(client):
    user = User(username='xpto', email='xpto@email.com')
    db.session.add(user)
    db.session.commit()

    response = client.get(url_for(
        'blog.user_popup', username=user.username
    ))

    esperado = 'https://www.gravatar.com/avatar/56dae58a162acfe2bd37dc031cb46f35?d=identicon&amp;s=64'
    
    assert response.status_code == 200
    assert esperado in response.text
    assert '/user/xpto' in response.text
