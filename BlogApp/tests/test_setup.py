import pytest
from flask_injector import FlaskInjector
from app import app
from services.dependencies import configure_testing_isconfigured, configure_testing_notconfigured
from services.dependencies import configure_testing_repository

@pytest.fixture
def is_configured():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app, modules=[configure_testing_isconfigured, configure_testing_repository])
    with app.test_client() as is_configured:
        yield is_configured


@pytest.fixture
def is_not_configured():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app, modules=[configure_testing_notconfigured, configure_testing_repository])
    with app.test_client() as is_not_configured:
        yield is_not_configured


def test_config_exists(is_configured):
    response = is_configured.get('/setup', follow_redirects=True)
    assert is_configured.get('/home').data in response.data

def test_config_notexist(is_not_configured):
    response = is_not_configured.get('/setup', follow_redirects=True)
    assert is_not_configured.get('/home').data not in response.data
