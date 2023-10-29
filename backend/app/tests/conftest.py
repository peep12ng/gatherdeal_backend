import pytest

from ...app import create_app, db
from ..config import TestingConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(config=TestingConfig)

    return app