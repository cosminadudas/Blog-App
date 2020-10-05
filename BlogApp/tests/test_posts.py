import pytest
from flask_injector import FlaskInjector
from app import app
from services.dependencies_for_testing import checking_repository_configure


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    FlaskInjector(app=app, modules=[checking_repository_configure])
    with app.test_client() as client:
        yield client


def test_index_route(client):
    result_two = client.get('/home')
    assert b'post 1' in result_two.data
    result_three = client.get('/posts')
    assert b'post 1' in result_three.data

def test_add_post_route(client):
    response = client.post('/add', data=dict(
        title="Post 3",
        owner="Cosmina",
        content="This is the third post"), follow_redirects=True)
    assert b'Cosmina' in response.data
    assert b'Post 3' in response.data


def test_edit_post_route(client):
    response = client.post('/edit/2',
                           data=dict(title='updated',
                                     content='This is the second post'),
                           follow_redirects=True)
    assert b'updated' in response.data


def test_delete_post_route(client):
    response = client.post('/delete/3', follow_redirects=True)
    assert b'post 3' not in response.data


def test_view_post_route(client):
    response = client.get('/view/2')
    assert b'updated' in response.data
