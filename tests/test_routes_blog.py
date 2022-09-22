from contextlib import _RedirectStream
from urllib import response
from flask import current_app, url_for
from flask_login import current_user

from tests.fixtures import create_user, testing_client
from app.models import db, User


def test_rota_auth_register_deve_retornar_200(testing_client):
    """Renderiza um formulário de cadastro."""
    assert testing_client.get(url_for('auth.register')).status_code == 200


def test_rota_auth_register_deve_criar_usuario_e_retornar_302(testing_client):
    """Redireciona para a página de login quando o registro é feito."""
    form = dict(
        username='pessoa',
        email='pessoa@email.com',
        password='senha',
        password2='senha'
    )

    response = testing_client.post(url_for('auth.register'), data=form)
    
    assert User.query.filter_by(email=form.get('email')).count() == 1
    assert response.status_code == 302
    assert response.location == url_for('auth.login')


def test_rota_auth_login_deve_retornar_200(testing_client):
    """Renderiza o formulário de login."""
    assert testing_client.get(url_for('auth.login')).status_code == 200


def test_rota_auth_login_deve_logar_pessoa_e_retornar_302(testing_client):
    """Redireciona para o index quando os dados de login são autenticados."""
    form = dict(
        username="pessoa",
        password="senha"
    )

    response = testing_client.post(url_for('auth.login'), data=form)

    assert response.status_code == 302
    assert current_user.is_authenticated == True
    assert response.location == url_for('blog.index')


def test_rota_auth_logout_deve_deslogar_e_retornar_302(testing_client):
    """Redireciona para o index após encerrar a sessão atual"""
    response = testing_client.get(url_for('auth.logout'))
    
    assert current_user.is_authenticated == False
    assert response.status_code == 302
    assert response.location == url_for('blog.index')


def test_rota_auth_reset_password_request_deve_retornar_200(testing_client):
    """Carrega o formulario para solicitar a alteração de senha."""
    assert testing_client.get(
        url_for('auth.reset_password_request'
    )).status_code == 200


def test_rota_auth_reset_password_request_deve_retornar_302(testing_client):
    """Redireciona para o login quando um email é inserido."""
    form = dict(
        email='pessoa@email.com'
    )

    response = testing_client.post(
        url_for('auth.reset_password_request'), data=form
    )

    assert response.status_code == 302
    assert response.location == url_for('auth.login')


def test_rota_auth_reset_password_deve_retornar_302(testing_client):
    """Redireciona para o index quando um token não é válido."""
    token = 123

    response = testing_client.get(url_for('auth.reset_password', token=token))

    assert response.status_code == 302
    assert response.location == url_for('blog.index')


def test_rota_auth_reset_password_deve_retornar_200(testing_client):
    """Quando um token é válido, renderiza o formulário de alteração de senha."""
    user = User.query.filter_by(username='pessoa').first()
    token = user.get_reset_password_token()

    response = testing_client.get(url_for('auth.reset_password', token=token))

    assert response.status_code == 200


def test_rota_blog_index_deve_retornar_302(testing_client):
    """Se o usuário não estiver autenticado, redireciona para o login."""
    response = testing_client.get(url_for('blog.index'))

    assert response.status_code == 302
    assert url_for('auth.login') in response.location


def test_rota_blog_index_deve_retornar_200(testing_client):
    """Quando autenticado, renderiza o index com as postagens dos seguidores"""
    testing_client.post(
        url_for('auth.login'), data=dict(username='pessoa', password='senha')
    )

    response = testing_client.get(url_for('blog.index'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_discover_deve_retornar_200(testing_client):
    """Quando autenticado, renderiza o discover e todos os posts do blog"""
    response = testing_client.get(url_for('blog.explore'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_user_deve_retornar_200(testing_client):
    """Quando autenticado, renderiza a página do usuário"""
    response = testing_client.get(
        url_for('blog.user', username=current_user.username)
    )

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_edit_profile_deve_retornar_200(testing_client):
    """Quando autenticado, renderiza uma formulário para editar o perfil"""
    response = testing_client.get(url_for('blog.edit_profile'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200
