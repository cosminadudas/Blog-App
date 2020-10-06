import pytest
from flask_injector import FlaskInjector
from app import app
from services.dependencies import configure_testing_database
from services.dependencies import configure_testing_repository

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app, modules=[configure_testing_database, configure_testing_repository])
    with app.test_client() as client:
        yield client


def test_setup_route(client):
    response = client.get('/setup', follow_redirects=True)
    assert client.get('/home').data in response.data
