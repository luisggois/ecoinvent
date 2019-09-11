from dotenv import load_dotenv
import os

'''
:SECRET_KEY: protect against modyfing cookies, cross-site requests and other attacks
:SQLALCHEMY_DATABASE_URI: specify location for the database (connection string)
:ALLOWED_EXTENSIONS: specify file extensions supported by the back-end
:BCRYPT_LOG_ROUNDS: specify the number of rounds that the algorithm executes in hashing a password
:ENV: environment mode
:DEBUG: debug mode
:WTF_CSRF_ENABLED: csrf protection mode
'''

load_dotenv(verbose=True, override=True)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")
    ALLOWED_EXTENSIONS = ('.spold')
    BCRYPT_LOG_ROUNDS = 12
    ENV = 'production'
    DEBUG = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    TESTING = True
    WTF_CSRF_ENABLED = False
