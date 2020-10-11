def test_add_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    the_password = '07D046D5FAC12B3F82DAF5035B9AAE86DB5ADC8275EBFBF05EC83005A4A8BA3E'
    response = is_config.post('/add/user', data=dict(name='david',
                                                     email='david@yahoo.com',
                                                     password=the_password),
                              follow_redirects=True)
    assert b'david' in response.data


def test_add_user_route_when_config_file_exists_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='cosmina',
                                       password='cosmina'), follow_redirects=True)
    the_password = '07D046D5FAC12B3F82DAF5035B9AAE86DB5ADC8275EBFBF05EC83005A4A8BA3E'
    response = is_config.post('/add/user', data=dict(name='david',
                                                     email='david@yahoo.com',
                                                     password=the_password),
                              follow_redirects=True)
    assert b'Email' in response.data


def test_add_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    the_password = '07D046D5FAC12B3F82DAF5035B9AAE86DB5ADC8275EBFBF05EC83005A4A8BA3E'
    response = is_not_config.post('/add/user', data=dict(name='david',
                                                         email='david@yahoo.com',
                                                         password=the_password),
                                  follow_redirects=True)
    assert b'Database' in response.data


def test_edit_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    the_password = 'D259039D17A64F94A3B3BB7F00C4A3C99208B8809254A6766AD6400D8393B5A7'
    response = is_config.post('/edit/user/2', data=dict(name='dudas',
                                                        email='dudas@yahoo.com',
                                                        new_password=the_password,
                                                        confirm_password=the_password),
                              follow_redirects=True)
    assert b'dudas' in response.data


def test_edit_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='david',
                                       password='david'), follow_redirects=True)
    the_password = 'D259039D17A64F94A3B3BB7F00C4A3C99208B8809254A6766AD6400D8393B5A7'
    response = is_config.post('/edit/user/3', data=dict(name='dudas',
                                                        email='dudas@yahoo.com',
                                                        new_password=the_password,
                                                        confirm_password=the_password),
                              follow_redirects=True)
    assert b'Email' in response.data


def test_edit_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    the_password = '07D046D5FAC12B3F82DAF5035B9AAE86DB5ADC8275EBFBF05EC83005A4A8BA3E'
    response = is_not_config.post('/edit/user/2', data=dict(name='david',
                                                            email='david@yahoo.com',
                                                            password=the_password),
                                  follow_redirects=True)
    assert b'Database' in response.data


def test_delete_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('/delete/user/4',
                             follow_redirects=True)
    assert b'david' in response.data


def test_delete_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='david',
                                       password='david'), follow_redirects=True)
    response = is_config.get('/delete/user/3',
                             follow_redirects=True)
    assert b'Email' in response.data


def test_delete_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('/delete/user/2',
                                 follow_redirects=True)
    assert b'Database' in response.data


def test_view_user_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('/view/user/2',
                             follow_redirects=True)
    assert b'dudas' in response.data


def test_view_user_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='david',
                                       password='david'), follow_redirects=True)
    response = is_config.get('/view/user/3',
                             follow_redirects=True)
    assert b'Email' in response.data


def test_view_user_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('/view/user/2',
                                 follow_redirects=True)
    assert b'Database' in response.data


def test_view_all_users_route_when_config_file_and_admin_exists(is_config):
    is_config.post('/login', data=dict(username_or_email='admin',
                                       password='admin'), follow_redirects=True)
    response = is_config.get('/view/users',
                             follow_redirects=True)
    assert b'dudas' in response.data


def test_view_all_users_route_when_config_file_exist_and_user_not_admin(is_config):
    is_config.post('/login', data=dict(username_or_email='david',
                                       password='david'), follow_redirects=True)
    response = is_config.get('/view/users',
                             follow_redirects=True)
    assert b'Email' in response.data


def test_view_all_users_route_when_config_file_not_exist(is_not_config):
    is_not_config.post('/login', data=dict(username_or_email='admin',
                                           password='admin'), follow_redirects=True)
    response = is_not_config.get('/view/users',
                                 follow_redirects=True)
    assert b'Database' in response.data
