import os

class Config:
    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True

    JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']

    UPLOADED_IMAGES_DEST = 'static/images'

    CACHE_TYPE = 'simple'   # Default CACHE_TYPE is Null

    CACHE_DEFAULT_TIMEOUT = 10*60 # Expiration time is 10 minutes

    RATELIMIT_HEADERS_ENABLED = True

class DevelopmentConfig(Config):
    """
    Extends the parent Config class.
    The DEBUG value is set to True. This will allow
    us to see the error messages while we are developing
    """
    DEBUG = True

    SECRET_KEY = 'super-secret-key'

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://Shayan_Riyaz:empirestate@localhost:5432/TheDailyCook'

class StagingConfig(Config):

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    """
    Extends the parent class. In production environment
    these values are obtained from the environment variables.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')








