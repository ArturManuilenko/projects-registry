import logging


class Config(object):
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
    # DELETE_FRESH_EXPIRES = timedelta(days=1)
    # JWT_SECRET_KEY = sha256(environ.get("APPLICATION_SECRET_KEY").encode('UTF-8')).hexdigest()
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    # BUNDLE_ERRORS = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestConfig(Config):
    SERVER_NAME = 'localhost'
    SESSION_COOKIE_DOMAIN = False
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
