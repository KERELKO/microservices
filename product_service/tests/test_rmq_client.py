from src.services.impl import RPCAuthClient


def test_rpc_auth_client():
    service = RPCAuthClient()
    user_data = {
        'username': 'carbi',
        'password': '1234',
    }
    response_json = service.call(data=user_data)
    print(response_json)
    assert 'token' in response_json
    assert isinstance(response_json['token'], str), response_json['token']


test_rpc_auth_client()
