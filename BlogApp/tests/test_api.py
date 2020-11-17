def test_api_route_when_config_file_exists(is_config):
    result = is_config.get('/API/post/1')
    post_data = result.json
    assert post_data["owner"] == "david"

def test_api_route_when_config_file_does_not_exist(is_not_config):
    result = is_not_config.get('/API/post/1', follow_redirects=True)
    assert b'User' in result.data

def test_api_route_when_config_file_exists_and_id_not_exist(is_config):
    result = is_config.get('/API/post/25')
    assert b'404' in result.data
