import pytest
from flask import request
from app import app
from views import posts
from repository.blog_posts_factory import blog_posts_factory

ACTION_TYPE = "testing"
posts.blog_posts = blog_posts_factory(ACTION_TYPE)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    result_one = client.get('/')
    assert b'post 1' in result_one.data
    result_two = client.get('/home')
    assert b'post 1' in result_two.data
    result_three = client.get('/posts')
    assert b'post 1' in result_three.data


def test_add_post_route(client):
    response = client.post('/add', data=dict(
        title="Post 3", 
        owner="Cosmina", 
        content="This is the third post"), 
        follow_redirects=True)
    
    assert b'Cosmina' in response.data
    assert b'Post 3' in response.data


def test_edit_post_route(client):
    assert client.get('/edit/2', follow_redirects=True).status_code == 200
    response = client.post('/edit/2', data=dict(title='updated', content='This is the second post'), follow_redirects=True)
    with app.test_client() as client:
        client.get('/?post_id=2', follow_redirects=True)
        assert request.args['post_id'] == '2'
    assert b'updated' in response.data


def test_delete_post_route(client):
    response = client.post('/delete/3', follow_redirects=True)
    assert b'post 3' not in response.data