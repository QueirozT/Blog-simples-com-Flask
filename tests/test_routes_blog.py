from flask import current_app, url_for
from flask_login import current_user
from time import time

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
    
    assert User.query.filter_by(email=form.get('email')).count() == 1
    assert response.status_code == 302
    assert response.location == url_for('auth.login')


def test_rota_auth_login_deve_retornar_200(client):
    """Renderiza o formulário de login."""
    assert client.get(url_for('auth.login')).status_code == 200


def test_rota_auth_login_deve_logar_pessoa_e_retornar_302(client):
    """Redireciona para o index quando os dados de login são autenticados."""
    form = dict(
        username="pessoa",
        password="senha"
    )

    response = client.post(url_for('auth.login'), data=form)

    assert response.status_code == 302
    assert current_user.is_authenticated == True
    assert response.location == url_for('blog.index')


def test_rota_auth_logout_deve_deslogar_e_retornar_302(client):
    """Redireciona para o index após encerrar a sessão atual"""
    response = client.get(url_for('auth.logout'))
    
    assert current_user.is_authenticated == False
    assert response.status_code == 302
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

    assert response.status_code == 302
    assert response.location == url_for('auth.login')


def test_rota_auth_reset_password_deve_retornar_302(client):
    """Redireciona para o index quando um token não é válido."""
    token = 123

    response = client.get(url_for('auth.reset_password', token=token))

    assert response.status_code == 302
    assert response.location == url_for('blog.index')


def test_rota_auth_reset_password_deve_retornar_200(client):
    """Quando um token é válido, renderiza o formulário de alteração de senha."""
    user = User.query.filter_by(username='pessoa').first()
    token = user.get_reset_password_token()

    response = client.get(url_for('auth.reset_password', token=token))

    assert response.status_code == 200


def test_rota_blog_index_deve_retornar_302(client):
    """Se o usuário não estiver autenticado, redireciona para o login."""
    response = client.get(url_for('blog.index'))

    assert response.status_code == 302
    assert url_for('auth.login') in response.location


def test_rota_blog_index_deve_retornar_200(client):
    """Quando autenticado, renderiza o index com as postagens dos seguidores"""
    client.post(
        url_for('auth.login'), data=dict(username='pessoa', password='senha')
    )

    response = client.get(url_for('blog.index'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_discover_deve_retornar_200(client):
    """Quando autenticado, renderiza o discover e todos os posts do blog"""
    response = client.get(url_for('blog.explore'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_user_deve_retornar_200(client):
    """Quando autenticado, renderiza a página do usuário"""
    response = client.get(
        url_for('blog.user', username=current_user.username)
    )

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_edit_profile_deve_retornar_200(client):
    """Quando autenticado, renderiza uma formulário para editar o perfil"""
    response = client.get(url_for('blog.edit_profile'))

    assert current_user.is_authenticated == True
    assert response.status_code == 200


def test_rota_blog_notifications_deve_retornar_200_e_uma_lista_vazia(client):
    """Esta rota deve retornar uma lista de notificações vazias"""
    response = client.get(url_for('blog.notifications'))

    esperado = []
    
    assert response.status_code == 200
    assert response.json == esperado


def test_rota_blog_notifications_deve_retornar_200_e_uma_lista_de_json(client):
    """Esta rota deve retornar uma lista de notificações em formato json"""
    current_user.add_notification('mensagem de teste', 0)

    response = client.get(url_for('blog.notifications'))

    esperado = [{
        'data': 0, 
        'name': 'mensagem de teste', 
        'timestamp': current_user.notifications.first().timestamp
    }]

    
    assert response.status_code == 200
    assert response.json == esperado


def test_rota_messages_deve_retornar_200_e_um_template_sem_mensagens(client):
    """Esta rota deve renderizar um template mas não conter nenhuma mensagem"""
    response = client.get(url_for('blog.messages'))
    
    esperado = 'Você ainda não tem mensagens para exibir...'
    
    assert response.status_code == 200
    assert esperado in response.data.decode('utf-8')


def test_rota_send_message_deve_retornar_200_quando_enviar_uma_mensagem(client):
    """Esta rota registra as mensagens privadas dos usuarios no banco de dados"""

    response = client.post(
        url_for('blog.send_message', recipient=current_user.username), 
        data={'body': 'mensagem de teste'}
    )

    assert response.status_code == 200


def test_rota_user_popup_deve_retornar_200_e_o_perfil_do_usuario(client):
    """Esta rota renderiza um popup com mini perfil do usuário"""
    response = client.get(url_for(
        'blog.user_popup', username=current_user.username
    ))

    esperado = current_user.username

    assert response.status_code == 200
    assert esperado in response.data.decode('utf-8')
