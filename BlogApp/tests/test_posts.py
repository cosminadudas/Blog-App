import pytest
from app import app
from views import posts
from repository.blog_posts_factory import factory

ACTION_TYPE = "testing"
posts.blog_posts = factory(ACTION_TYPE)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    result_one = client.get('/')
    assert b'post 1' in result_one.data
    assert b'post 2' in result_one.data
    result_two = client.get('/home')
    assert b'post 1' in result_two.data
    assert b'post 2' in result_two.data
    result_three = client.get('/posts')
    assert b'post 1' in result_three.data
    assert b'post 2' in result_three.data


