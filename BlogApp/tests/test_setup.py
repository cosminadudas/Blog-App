import pytest
from flask_injector import FlaskInjector
from app import app
from services.dependencies import checking_database_configure
from services.dependencies import checking_repository_configure

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app, modules=[checking_database_configure, checking_repository_configure])
    with app.test_client() as client:
        yield client


def test_setup_route(client):
    response = client.get('/setup', follow_redirects=True)
    assert client.get('/home').data in response.data
