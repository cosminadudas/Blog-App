
def test_setup_when_config_file_exists(is_config):
    response = is_config.get('/setup', follow_redirects=True)
    assert is_config.get('/home').data in response.data


def test_setup_when_config_file_not_exist(is_not_config):
    response = is_not_config.get('/setup', follow_redirects=True)
    assert b'User' in response.data
