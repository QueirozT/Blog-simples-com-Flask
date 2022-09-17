from decouple import config


class Config(object):
    DEBUG = config(
        'DEBUG',
        cast=bool,
        default=True
    )
    
    SECRET_KEY = config(
        'SECRET_KEY', 
        default="você-nuna-vai-adivinhar"
    )

    BABEL_DEFAULT_LOCALE ='pt_BR'

    SQLALCHEMY_DATABASE_URI = config(
        'DATABASE_URL', 
        default="sqlite:///../database.db"
    )
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


    POSTS_PER_PAGE = 20