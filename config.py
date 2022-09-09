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
