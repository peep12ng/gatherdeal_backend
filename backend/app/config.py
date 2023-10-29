import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig(object):

    # app name
    PROJECT = "app"

    PROJECT_ROOT = os.path.dirname(__file__)

    DEBUG = False
    TESTING = False

    # ADMINS = ["peep12ng@gmail.com"]

class DefaultConfig(BaseConfig):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalConfig(DefaultConfig):

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_LOCAL_URL")

class TestingConfig(DefaultConfig):

    PROJECT = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TESTING_URL")

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