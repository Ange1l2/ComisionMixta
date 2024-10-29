from decouple import config


class Config(object):
    DEBUG = config('DEBUG')
    Testing = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5407df0348c2d8a31b0339e189'  # Agregar esta línea

    FLASK_RUN_PORT = config('FLASK_RUN_PORT')

    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = 465  # int(config('MAIL_PORT'))
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_USE_TLS = False  # config('MAIL_USE_TLS')
    MAIL_USE_SSL = True  # config('MAIL_USE_SSL')
    # Fue necesario poner esta para flask-mail
    # SOLUCIÓN para poner mail = MAIL(app) después de app.config.from_object(app_settings)
    MAIL_DEBUG = int(config('MAIL_DEBUG'))

    print(type(DEBUG))


class DevelopmentConfig(Config):
    DEVELOPMENT = True


config = {
    'development': DevelopmentConfig
}
