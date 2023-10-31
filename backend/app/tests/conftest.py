import pytest

from app import create_app
from app import db as _db
from ..config import TestingConfig

import os
import shutil
from flask_migrate import init, migrate, upgrade

@pytest.fixture(scope='session')
def app():
    app = create_app(config=TestingConfig)

    os.chdir(os.path.split(os.path.abspath(__file__))[0])

    with app.app_context():
        init()
        migrate()
        upgrade()

        yield app

    shutil.rmtree("migrations")

@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db

@pytest.fixture(scope='function')
def session(app, db, request):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db._make_scoped_session(options)

    _db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()