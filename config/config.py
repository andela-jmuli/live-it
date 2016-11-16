import os
# set project base directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    " default settings "
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")
    ERROR_404_HELP = False
    ERROR_400_HELP = False


class TestingConfig(object):
    " testing  configurations "
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "test_bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(object):
    " development configuration "
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config_settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'SECRET_KEY': "k9we213@#21tjuw"
}
