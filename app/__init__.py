from flask import Flask
from config import Config
from flask_babel import Babel
from flask_misaka import Misaka
from flask_migrate import Migrate
from flask_moment import Moment
from flask_pagedown import PageDown
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pathlib import Path

from app.auth import bp_auth
from app.errors import bp_errors
from .blog import bp_blog

from .email import config as config_mail
from .models import config as config_db


babel = Babel()
migrate = Migrate()
moment = Moment()
pagedown = PageDown()
misaka = Misaka(
    no_html=True, 
    fenced_code=True, 
    underline=True,
    highlight=True,
    quote=True,
    no_indented_code=True,
    space_headers=True,
    strikethrough=True,
    tables=True,
)

def create_app(config_class=Config):
    app = Flask(__name__)

    # Carregando as configurações
    app.config.from_object(config_class)
    
    # Configurando o Babel para tradução
    babel.init_app(app)

    # Configurando o flask Moment para tratamento de datas
    moment.init_app(app)

    # Configurando o flask pagedown para criação de Markdown
    pagedown.init_app(app)

    # Configurando o flask misaka para exibição do Markdown
    misaka.init_app(app)

    # Configurando o Migrate para o SQLAlchemy
    config_db(app)
    migrate.init_app(app, app.db)

    # Configurando o envio dos emails 
    config_mail(app)

    # Registrando as blueprints
    app.register_blueprint(bp_blog)
    app.register_blueprint(bp_errors)
    app.register_blueprint(bp_auth, url_prefix='/auth')

    # Configurando o servidor de email
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['ADMINS'][0],
                toaddrs=app.config['ADMINS'], subject='Falha no Blog',
                credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    # Configurando o arquivo de log
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        PATH_LOGS = Path.joinpath(
            Path(__file__).parent.parent, 'logs/'
        )
        Path.mkdir(PATH_LOGS, exist_ok=True)
        file_handler = RotatingFileHandler(
            f'{PATH_LOGS}/blog.log', maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Inicialização do Blog')

    return app
