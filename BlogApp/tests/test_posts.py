
def test_index_route_when_config_file_exists(is_config):
    result_one = is_config.get('/home')
    assert b'post 1' in result_one.data
    result_two = is_config.get('/posts')
    assert b'post 1' in result_two.data


def test_add_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(
        username_or_email='cosmina',
        password='cosmina'), follow_redirects=True)
    response = is_config.post('/add/post', data=dict(
        title="Post 3",
        owner="Cosmina",
        content="This is the third post"), follow_redirects=True)
    assert b'Post 3' in response.data


def test_add_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/add/post', follow_redirects=True)
    assert is_config.get('/login').data in response.data


def test_edit_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(
        username_or_email='cosmina',
        password='cosmina'), follow_redirects=True)
    response = is_config.post('/edit/post/2',
                              data=dict(title='updated',
                                        content='This is the second post'),
                              follow_redirects=True)
    assert b'updated' in response.data


def test_edit_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/edit/post/2', follow_redirects=True)
    assert is_config.get('/login').data in response.data

def test_edit_post_route_when_config_file_exists_and_user_is_not_admin_or_owner(is_config):
    is_config.post('/login', data=dict(
        username_or_email='larisa',
        password='larisa'), follow_redirects=True)
    response = is_config.post('/edit/post/2',
                              data=dict(title='updated',
                                        content='This is the second post'),
                              follow_redirects=True)
    assert b'403' in response.data


def test_delete_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(username_or_email='cosmina',
                                       password='cosmina'), follow_redirects=True)
    response = is_config.post('/delete/post/3', follow_redirects=True)
    assert b'post 3' not in response.data


def test_delete_post_route_when_config_file_exists_and_user_is_not_admin_or_owner(is_config):
    is_config.post('/login', data=dict(
        username_or_email='larisa',
        password='larisa'), follow_redirects=True)
    response = is_config.get('/delete/post/2',
                             follow_redirects=True)
    assert b'403' in response.data

def test_delete_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/delete/post/3', follow_redirects=True)
    assert is_config.get('/login').data in response.data


def test_view_post_route_when_config_file_exists(is_config):
    response = is_config.get('/view/post/2')
    assert b'updated' in response.data


def test_index_route_when_config_file_not_exist(is_not_config):
    result_one = is_not_config.get('/', follow_redirects=True)
    assert b'User' in result_one.data
    result_two = is_not_config.get('/posts', follow_redirects=True)
    assert b'Password' in result_two.data


def test_add_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/add/post', follow_redirects=True)
    assert b'User' in result.data


def test_edit_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/edit/post/1', follow_redirects=True)
    assert b'User' in result.data


def test_delete_route_when_config_file_not_exist(is_not_config):
    result = is_not_config.get('/delete/post/1', follow_redirects=True)
    assert b'User' in result.data


def test_view_post_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.get('/view/post/2', follow_redirects=True)
    assert b'User' in response.data
