import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '0cf31b2c283ce3431794586df7b0996d'
    SSL = False
    MQTT_REFRESH_TIME = 0.1

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'DB': 'flaskhab-dev'}


class ProductionConfig(Config):
    MONGODB_SETTINGS = {'DB': 'flaskhab'}


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {'DB': 'flaskhab-test'}


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
