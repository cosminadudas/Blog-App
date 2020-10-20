def test_first_login_setup_get_route_without_login_attempt_when_config_file_exists(is_config):
    response = is_config.get('/users/first_login_setup/1', follow_redirects=True)
    assert b'405' in response.data


def test_first_login_setup_post_route_without_login_attempt_when_config_file_exists(is_config):
    response = is_config.post('/users/first_login_setup/1',
                              data=dict(email='admin@yahoo.com',
                                        password='admin',
                                        confirm_password='admin'),
                              follow_redirects=True)
    assert b'400' in response.data


def test_first_login_setup_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.post('/users/first_login_setup/1',
                                  data=dict(email='admin@yahoo.com',
                                            password='admin',
                                            confirm_password='admin'),
                                  follow_redirects=True)
    assert b'Database' in response.data


def test_add_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.post('users/add', data=dict(name='david',
                                                     email='david@yahoo.com',
                                                     password='david'),
                              follow_redirects=True)
    assert b'david' in response.data


def test_add_user_route_when_config_file_exists_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='cosmina',
                                       password='cosmina'), follow_redirects=True)
    response = is_config.post('users/add', data=dict(name='david',
                                                     email='david@yahoo.com',
                                                     password='david'),
                              follow_redirects=True)
    assert b'403' in response.data


def test_add_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.post('users/add', data=dict(name='david',
                                                         email='david@yahoo.com',
                                                         password='david'),
                                  follow_redirects=True)
    assert b'Database' in response.data


def test_edit_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.post('users/edit/7', data=dict(name='dudas',
                                                        email='dudas@yahoo.com',
                                                        new_password='dudas',
                                                        confirm_password='dudas'),
                              follow_redirects=True)
    assert b'dudas' in response.data


def test_edit_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='maria',
                                       password='larisa'), follow_redirects=True)
    response = is_config.post('users/edit/3', data=dict(name='dudas',
                                                        email='dudas@yahoo.com',
                                                        new_password='dudas',
                                                        confirm_password='dudas'),
                              follow_redirects=True)
    assert b'403' in response.data


def test_edit_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.post('users/edit/2', data=dict(name='david',
                                                            email='david@yahoo.com',
                                                            password='david'),
                                  follow_redirects=True)
    assert b'Database' in response.data


def test_delete_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('users/delete/5',
                             follow_redirects=True)
    assert b'david' in response.data


def test_delete_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='maria',
                                       password='larisa'), follow_redirects=True)
    response = is_config.get('users/delete/3',
                             follow_redirects=True)
    assert b'403' in response.data


def test_delete_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('users/delete/2',
                                 follow_redirects=True)
    assert b'Database' in response.data


def test_view_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('users/view/7',
                             follow_redirects=True)
    assert b'dudas' in response.data


def test_view_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='mihai',
                                       password='mihai'), follow_redirects=True)
    response = is_config.get('users/view/3',
                             follow_redirects=True)
    assert b'403' in response.data


def test_view_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('users/view/2',
                                 follow_redirects=True)
    assert b'Database' in response.data


def test_view_all_users_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('users/view',
                             follow_redirects=True)
    assert b'dudas' in response.data


def test_view_all_users_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='mihai',
                                       password='mihai'), follow_redirects=True)
    response = is_config.get('users/view',
                             follow_redirects=True)
    assert b'403' in response.data


def test_view_all_users_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('users/view',
                                 follow_redirects=True)
    assert b'Database' in response.data


def test_add_user_route_when_config_file_exists_and_no_user_is_registered(is_config):
    response = is_config.post('users/add', data=dict(name='david',
                                                     email='david@yahoo.com',
                                                     password='david'),
                              follow_redirects=True)
    assert b'Email' in response.data


def test_edit_user_route_when_config_file_and_no_user_is_registered(is_config):
    response = is_config.post('users/edit/7', data=dict(name='dudas',
                                                        email='dudas@yahoo.com',
                                                        new_password='dudas',
                                                        confirm_password='dudas'),
                              follow_redirects=True)
    assert b'Email' in response.data


def test_delete_user_route_when_config_file_and_no_user_is_registered(is_config):
    response = is_config.get('users/delete/5',
                             follow_redirects=True)
    assert b'Email' in response.data


def test_view_user_route_when_config_file_and_no_user_is_registered(is_config):
    response = is_config.get('users/view/7',
                             follow_redirects=True)
    assert b'Email' in response.data


def test_view_all_users_route_when_config_file_and_no_user_is_registered(is_config):
    response = is_config.get('users/view',
                             follow_redirects=True)
    assert b'Email' in response.data
