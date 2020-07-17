
import secrets

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY= str(secrets.token_urlsafe(1024))
    

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False