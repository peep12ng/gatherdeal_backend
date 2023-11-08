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

    PROJECT = "local"
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_LOCAL_URL")

class TestingConfig(DefaultConfig):

    TESTING = True
    PROJECT = "test"

class DevelopmentConfig(DefaultConfig):

    TESTING = True
    PROJECT = "dev"
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DEV_URL")

class ProdConfig(DefaultConfig):

    DEBUG = False
    PROJECT = "prod"
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PROD_URL")

def get_config(MODE):
    SWITCH = {
        "LOCAL":LocalConfig,
        "TESTING":TestingConfig,
        "DEV":DevelopmentConfig,
        "PROD":ProdConfig,
    }
    return SWITCH[MODE]