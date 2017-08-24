class BaseConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/flaskapi3'
    SECRET_KEY = "Thisismysecret"


class TestConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/test_api'


class DevelopmentConfig(BaseConfig):
    """Configurations for Development."""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Configurations for Production."""
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
}