import os

from ..config import TestingConfig

def test_testing_config(app):
    app.config.from_object(TestingConfig)

    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")