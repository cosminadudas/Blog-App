def test_index_route_when_config_file_exists(is_config):
    result_one = is_config.get('/home')
    assert b'post 1' in result_one.data
    assert b'updated' in result_one.data
    assert b'post 3' in result_one.data
    assert b'post 4' in result_one.data
    assert b'post 6' not in result_one.data
    assert b'Next' in result_one.data
    result_two = is_config.get('/posts')
    assert b'post 1' in result_two.data


def test_second_page_of_index_route_when_filter_is_not_activated_and_config_file_exists(is_config):
    response = is_config.get('/home?page=1')
    assert b'post 5' in response.data
    assert b'post 6' in response.data
    assert b'post 7' in response.data
    assert b'post 8' in response.data
    assert b'post 9' in response.data
    assert b'post 10' not in response.data
    assert b'Next' in response.data
    assert b'Previous' in response.data


def test_second_page_of_index_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.get('/home?page=1', follow_redirects=True)
    assert b'Database' in response.data


def test_index_route_when_config_file_exists_and_filter_is_activated(is_config):
    response = is_config.get('/home?user=ion')
    assert b'ion' in response.data
    assert b'post 4' in response.data
    assert b'post 3' in response.data
    assert b'post 5' not in response.data


def test_first_page_of_index_route_when_filter_activated_and_are_less_than_five_posts(is_config):
    response = is_config.get('/home?user=ion', follow_redirects=True)
    assert b'Next' not in response.data
    assert b'Previous' not in response.data


def test_first_page_of_index_route_when_filter_activated_and_are_more_than_five_posts(is_config):
    response = is_config.get('/home?user=alex', follow_redirects=True)
    assert b'Next' in response.data
    assert b'Previous' not in response.data


def test_first_page_of_index_route_when_filter_is_not_activated(is_config):
    response = is_config.get('/home', follow_redirects=True)
    assert b'Next' in response.data
    assert b'Previous' not in response.data


def test_second_page_of_index_route_when_config_file_exists_and_filter_is_activated(is_config):
    response = is_config.get('/home?page=1&user=alex')
    assert b'post 10' in response.data
    assert b'post 11' in response.data
    assert b'post 12' in response.data
    assert b'post 13' in response.data
    assert b'post 14' in response.data
    assert b'Next' in response.data
    assert b'Previous' in response.data


def test_third_page_of_index_route_when_filter_activated_and_are_less_than_five_posts(is_config):
    response = is_config.get('/home?page=2&user=alex')
    assert b'post 15' in response.data
    assert b'post 16' in response.data
    assert b'post 17' in response.data
    assert b'Next' not in response.data
    assert b'Previous' in response.data


def test_index_route_when_requested_page_is_negative(is_config):
    response = is_config.get('/home?page=-1')
    assert is_config.get('/home?page=0').data in response.data


def test_index_route_when_requested_page_is_higher_than_last_page(is_config):
    response = is_config.get('/home?page=8')
    assert is_config.get('/home?page=0').data in response.data


def test_add_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(
        username_or_email='cosmina',
        password='cosmina'), follow_redirects=True)
    response = is_config.post('/add', data=dict(
        title="Post 3",
        content="This is the third post"), follow_redirects=True)
    assert b'Post 3' in response.data


def test_add_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/add', follow_redirects=True)
    assert is_config.get('/login').data in response.data


def test_edit_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(
        username_or_email='cosmina',
        password='cosmina'), follow_redirects=True)
    response = is_config.post('/edit/2',
                              data=dict(title='updated',
                                        content='This is the second post'),
                              follow_redirects=True)
    assert b'updated' in response.data


def test_edit_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/edit/2', follow_redirects=True)
    assert is_config.get('/login').data in response.data


def test_edit_post_route_when_config_file_exists_and_user_is_not_admin_or_owner(is_config):
    is_config.post('/login', data=dict(
        username_or_email='larisa',
        password='larisa'), follow_redirects=True)
    response = is_config.post('/edit/2',
                              data=dict(title='updated',
                                        content='This is the second post'),
                              follow_redirects=True)
    assert b'403' in response.data


def test_delete_post_route_when_config_file_and_admin_or_owner_exist(is_config):
    is_config.post('/login', data=dict(username_or_email='cosmina',
                                       password='cosmina'), follow_redirects=True)
    response = is_config.post('/delete/3', follow_redirects=True)
    assert b'post 3' not in response.data


def test_delete_post_route_when_config_file_exists_and_user_is_not_admin_or_owner(is_config):
    is_config.post('/login', data=dict(
        username_or_email='larisa',
        password='larisa'), follow_redirects=True)
    response = is_config.get('/delete/2',
                             follow_redirects=True)
    assert b'403' in response.data


def test_delete_post_route_when_config_file_exists_and_user_not_exist(is_config):
    is_config.get('/logout')
    response = is_config.get('/delete/3', follow_redirects=True)
    assert is_config.get('/login').data in response.data


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
