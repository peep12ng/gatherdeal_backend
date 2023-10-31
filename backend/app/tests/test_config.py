import os

from ..config import LocalConfig, TestingConfig, DefaultConfig

def test_local_config(app):
    app.config.from_object(LocalConfig)
    
    assert app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_LOCAL_URL")

def test_testing_config(app):
    app.config.from_object(TestingConfig)

    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TESTING_URL")

def test_default_config(app):
    app.config.from_object(DefaultConfig)

    assert app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")