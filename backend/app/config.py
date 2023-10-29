import os

class BaseConfig(object):

    # app name
    PROJECT = "app"

    PROJECT_ROOT = os.path.dirname(__file__)

    DEBUG = False
    TESTING = False

    # ADMINS = ["peep12ng@gmail.com"]

class DefaultConfig(BaseConfig):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mariadb+pymysql://hotdeal:Qlalfqjsgh!23@sdavids.synology.me:3306/hotdeal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalConfig(DefaultConfig):

    SQLALCHEMY_DATABASE_URI = "mariadb+pymysql://root:password@localhost:3306/hotdeal"

class TestingConfig(DefaultConfig):

    PROJECT = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mariadb+pymysql://root:password@localhost:3306/hotdeal_test"

class StagingConfig(DefaultConfig):
    pass

class ProdConfig(DefaultConfig):
    pass

def get_config(MODE):
    SWITCH = {
        "LOCAL":LocalConfig,
        "TESTING":TestingConfig,
        "STAGING":StagingConfig,
        "PRODUCTION":ProdConfig,
    }
    return SWITCH[MODE]