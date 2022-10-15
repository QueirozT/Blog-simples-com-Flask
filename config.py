from decouple import config


class Config(object):
    DEBUG = config(
        'DEBUG', cast=bool, default=True
    )
    
    SECRET_KEY = config(
        'SECRET_KEY', default="você-nunca-vai-adivinhar"
    )

    BABEL_DEFAULT_LOCALE ='pt_BR'

    SQLALCHEMY_DATABASE_URI = config(
        'DATABASE_URL', default="sqlite:///../database.db"
    ).replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MAIL_SERVER = config('MAIL_SERVER', default='localhost')
    MAIL_PORT = config('MAIL_PORT', cast=int, default='8025')
    MAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool, default=False)
    MAIL_USERNAME = config('MAIL_USERNAME', default=None)
    MAIL_PASSWORD = config('MAIL_PASSWORD', default=None)
    ADMINS = config(
        'ADMINS', 
        cast=lambda v: [s.strip() for s in v.split(',')], 
        default="email@exemplo.com,"
    )

    LOG_TO_STDOUT = config('LOG_TO_STDOUT', cast=bool, default=False)


    POSTS_PER_PAGE = 20


class TestConfig(object):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    ADMINS = ['admin@email.com',]

    SECRET_KEY = "você-nunca-vai-adivinhar"

    BABEL_DEFAULT_LOCALE ='pt_BR'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    
    LOG_TO_STDOUT = True

    POSTS_PER_PAGE = 20
