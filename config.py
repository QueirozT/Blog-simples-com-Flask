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
