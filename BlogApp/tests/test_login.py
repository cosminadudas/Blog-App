
def test_login_route_when_config_file_exists(is_config):
    response = is_config.post('/login', data=dict(
        username_or_email="cosmina",
        password="cosmina"), follow_redirects=True)
    assert b'post 1' in response.data


def test_login_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.post('/login', data=dict(
        username_or_email="cosmina",
        password="cosmina"), follow_redirects=True)
    assert b'User' in response.data

def test_logout_route_when_config_file_exists(is_config):
    response = is_config.get('/logout', follow_redirects=True)
    assert b'post 1' in response.data


def test_logout_route_when_config_file_not_exist(is_not_config):
    response = is_not_config.get('/logout', follow_redirects=True)
    assert b'User' in response.data

def test_login_route_when_credentials_not_valid(is_config):
    response = is_config.post('/login', data=dict(
        username_or_email="cosmina",
        password="larisa"), follow_redirects=True)
    assert b"Wrong username/email or password! Try again!" in response.data
