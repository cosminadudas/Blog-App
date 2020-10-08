
def test_index_route_when_config_file_exists(is_config):
    result_one = is_config.get('/home')
    assert b'post 1' in result_one.data
    result_two = is_config.get('/posts')
    assert b'post 1' in result_two.data

def test_add_post_route_when_config_file_exists(is_config):
    response = is_config.post('/add', data=dict(
        title="Post 3",
        owner="Cosmina",
        content="This is the third post"), follow_redirects=True)
    assert b'Cosmina' in response.data
    assert b'Post 3' in response.data


def test_edit_post_route_when_config_file_exists(is_config):
    response = is_config.post('/edit/2',
                              data=dict(title='updated',
                                        content='This is the second post'),
                              follow_redirects=True)
    assert b'updated' in response.data


def test_delete_post_route_when_config_file_exists(is_config):
    response = is_config.post('/delete/3', follow_redirects=True)
    assert b'post 3' not in response.data


def test_view_post_route_when_config_file_exists(is_config):
    response = is_config.get('/view/2')
    assert b'updated' in response.data

def test_index_route_when_config_file_not_exist(is_not_config):
    result_one = is_not_config.get('/', follow_redirects=True)
    assert b'User' in result_one.data
    result_two = is_not_config.get('/posts', follow_redirects=True)
    assert b'Password' in result_two.data


def test_add_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/add', follow_redirects=True)
    assert b'User' in result.data


def test_edit_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/edit/1', follow_redirects=True)
    assert b'User' in result.data

def test_delete_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/delete/1', follow_redirects=True)
    assert b'User' in result.data


def test_view_post_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.get('/view/2', follow_redirects=True)
    assert b'User' in response.data
