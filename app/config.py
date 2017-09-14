class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = ('SECRET')
    SQLALCHEMY_DATABASE_URI = ('postgresql://postgres:admin@localhost/flask_api')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = ('postgres://ngecmlsgrrynmx:ba058d0a2414845849475e39c509a3c926895939ed7b0e1ceae23424a840e42d@ec2-54-163-227-202.compute-1.amazonaws.com:5432/d8jag19naeqkn6')
    SQLALCHEMY_DATABASE_URI = ('postgresql://postgres:admin@localhost/test_db')
    
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}