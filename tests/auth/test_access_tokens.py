from src.auth.service import AuthService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService.create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)


def test_decode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService.create_access_token(data)
    decoded_token = AuthService.decode_access_token(jwt_token)

    assert decoded_token
    assert isinstance(decoded_token, dict)
    assert decoded_token["user_id"] == 1
