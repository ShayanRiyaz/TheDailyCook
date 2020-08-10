class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://Shayan_Riyaz:empirestate@localhost:5432/TheDailyCook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']

    UPLOADED_IMAGES_DEST = 'static/images'

    CACHE_TYPE = 'simple'   # Default CACHE_TYPE is Null
    CACHE_DEFAULT_TIMEOUT = 10*60 # Expiration time is 10 minutes

    RATELIMIT_HEADERS_ENABLED = True



