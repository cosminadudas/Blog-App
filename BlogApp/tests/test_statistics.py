def test_statistics_route_when_logged_in_as_admin(is_config):
    is_config.post('/login', data=dict(
        username_or_email='admin',
        password='admin'), follow_redirects=True)
    response = is_config.get('/statistics')
    assert b'mircea' in response.data
    assert b'1' in response.data

def test_statistics_route_when_not_logged_in_as_admin(is_config):
    is_config.post('/login', data=dict(
        username_or_email='cosmina',
        password='cosmina'), follow_redirects=True)
    response = is_config.get('/statistics')
    assert b'403' in response.data

def test_statistics_route_when_not_logged_in(is_config):
    response = is_config.get('/statistics', follow_redirects=True)
    assert b'Password' in response.data

def test_statistics_route_when_config_file_not_exists(is_not_config):
    is_not_config.post('/login', data=dict(
        username_or_email='admin',
        password='admin'), follow_redirects=True)
    response = is_not_config.get('/statistics', follow_redirects=True)
    assert b'Database' in response.data
