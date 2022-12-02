from flask import url_for
from flask_login import current_user, login_user

from app.models import db, User


def test_rota_auth_register_deve_retornar_200(client):
    """Renderiza um formulário de cadastro."""
    assert client.get(url_for('auth.register')).status_code == 200


def test_rota_auth_register_deve_criar_usuario_e_retornar_302(client):
    """Redireciona para a página de login quando o registro é feito."""
    form = dict(
        username='pessoa',
        email='pessoa@email.com',
        password='senha',
        password2='senha'
    )

    response = client.post(url_for('auth.register'), data=form)
    
    esperado = 'You should be redirected automatically to the target URL: <a href="/auth/login">/auth/login</a>'
    
    assert User.query.filter_by(email=form.get('email')).count() == 1
    assert response.status_code == 302
    assert esperado in response.text
    assert response.location == url_for('auth.login')


def test_rota_auth_login_deve_retornar_200(client):
    """Renderiza o formulário de login."""
    assert client.get(url_for('auth.login')).status_code == 200


def test_rota_auth_login_deve_logar_e_retornar_302(client):
    """Redireciona para o index quando os dados de login são autenticados."""
    user = User(username='pessoa', email='pessoa@email.com')
    user.set_password('senha')
    db.session.add(user)
    db.session.commit()

    form = dict(
        email="pessoa@email.com",
        password="senha"
    )

    response = client.post(url_for('auth.login'), data=form)

    esperado = 'You should be redirected automatically to the target URL: <a href="/index">/index</a>'

    assert response.status_code == 302
    assert current_user.is_authenticated == True
    assert esperado in response.text
    assert response.location == url_for('blog.index')


def test_rota_auth_logout_deve_deslogar_e_retornar_302(client):
    """Redireciona para o index após encerrar a sessão atual"""
    user = User(username='pessoa', email='pessoa@email.com')
    login_user(user)

    response = client.get(url_for('auth.logout'))

    esperado = 'You should be redirected automatically to the target URL: <a href="/index">/index</a>'

    assert current_user.is_authenticated == False
    assert response.status_code == 302
    assert esperado in response.text
    assert response.location == url_for('blog.index')


def test_rota_auth_reset_password_request_deve_retornar_200(client):
    """Carrega o formulario para solicitar a alteração de senha."""
    assert client.get(
        url_for('auth.reset_password_request'
    )).status_code == 200


def test_rota_auth_reset_password_request_deve_retornar_302(client):
    """Redireciona para o login quando um email é inserido."""
    form = dict(
        email='pessoa@email.com'
    )

    response = client.post(
        url_for('auth.reset_password_request'), data=form
    )

    esperado = 'You should be redirected automatically to the target URL: <a href="/auth/login">/auth/login</a>'

    assert response.status_code == 302
    assert esperado in response.text
    assert response.location == url_for('auth.login')


def test_rota_auth_reset_password_deve_retornar_302(client):
    """Redireciona para o index quando um token não é válido."""
    token = 123

    response = client.get(url_for('auth.reset_password', token=token))

    esperado = 'You should be redirected automatically to the target URL: <a href="/index">/index</a>'

    assert response.status_code == 302
    assert esperado in response.text
    assert response.location == url_for('blog.index')


def test_rota_auth_reset_password_deve_retornar_200(client):
    """Quando um token é válido, renderiza o formulário de alteração de senha."""
    user = User(username='pessoa', email='pessoa@email.com')
    db.session.add(user)
    db.session.commit()

    token = user.get_reset_password_token()

    response = client.get(url_for('auth.reset_password', token=token))

    esperado = '<h1>Redefinir sua senha</h1>'

    assert response.status_code == 200
    assert esperado in response.text
