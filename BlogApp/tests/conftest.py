import pytest
from flask_injector import FlaskInjector
from app import app
from services.dependencies import configure_testing
from setup.database_config import DatabaseConfig


@pytest.fixture()
def is_config():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app,
                  modules=[configure_testing]).injector.get(DatabaseConfig).is_configured = True
    with app.test_client() as is_config:
        yield is_config


@pytest.fixture
def is_not_config():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app,
                  modules=[configure_testing]).injector.get(DatabaseConfig).is_configured = False
    with app.test_client() as is_not_config:
        yield is_not_config
