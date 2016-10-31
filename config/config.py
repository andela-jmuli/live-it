import os
# set project base directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    " default settings "
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "bucketlist.db")


class TestingConfig(object):
    " testing  configurations "
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test_bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "k9we213@#21tjuw"


class DevelopmentConfig(object):
    " development configuration "
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "k9we213@#21tjuw"

config_settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
