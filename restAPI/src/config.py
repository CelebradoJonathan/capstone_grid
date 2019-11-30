
import os


class Development(object):

    """

    Development environment configuration

    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:pgijtsaMS@localhost:5432/joborderdb"
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Production(object):

    """

    Production environment configurations

    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')



app_config = {

    'development': Development,

    'production': Production,

}