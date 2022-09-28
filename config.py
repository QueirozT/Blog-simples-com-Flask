from email.policy import default
from decouple import config


class Config(object):
    DEBUG = config(
        'DEBUG',
        cast=bool,
        default=True
    )
    
    SECRET_KEY = config(
        'SECRET_KEY', 
        default="você-nunca-vai-adivinhar"
    )

    BABEL_DEFAULT_LOCALE ='pt_BR'

    SQLALCHEMY_DATABASE_URI = config(
        'DATABASE_URL', 
        default="sqlite:///../database.db"
    ).replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = config('MAIL_PORT', cast=int, default=25)
    MAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool, default=False)
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    ADMINS = config(
        'ADMINS', 
        cast=lambda v: [s.strip() for s in v.split(',')], 
        default=[]
    )

    LOG_TO_STDOUT = config('LOG_TO_STDOUT', cast=bool, default=True)


    POSTS_PER_PAGE = 20


class TestConfig(object):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    ADMINS = ['admin@email.com',]

    SECRET_KEY = "você-nunca-vai-adivinhar"

    BABEL_DEFAULT_LOCALE ='pt_BR'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    
    POSTS_PER_PAGE = 20
