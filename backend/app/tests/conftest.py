import pytest

from app import create_app
from app import db
from ..config import TestingConfig

import os
import shutil
from flask_migrate import init, migrate, upgrade

from sqlalchemy import text

@pytest.fixture(scope='session')
def app():
    os.chdir(os.path.split(os.path.abspath(__file__))[0])

    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
    
    app = create_app(config=TestingConfig)

    with app.app_context():
        init()
        migrate()
        upgrade()

        yield app

        db.session.remove()
        db.drop_all()
        db.session.execute(text("DROP TABLE alembic_version"))

    shutil.rmtree("migrations")

@pytest.fixture(scope='session')
def session(app):
    with app.app_context():
        yield db.session

@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()

    return client