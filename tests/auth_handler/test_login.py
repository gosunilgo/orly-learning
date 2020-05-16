from http import HTTPStatus
import json

import pytest
import responses

from orlylearning.exceptions import InvalidCredentials
from orlylearning.handler import AuthHandler

@pytest.fixture(name='auth')
def init_auth():
    return AuthHandler(None, None)

@pytest.fixture(name='_response')
def init_response():
    with responses.RequestsMock() as rsps:
        rsps.add_callback(
            responses.POST, AuthHandler.OREILLY_LOGIN, callback=login_callback
        )
        yield rsps

def login_callback(request):
    request_body = json.loads(request.body)
    if (
            'valid' in request_body.get('email', '')
            and 'valid' in request_body.get('password', '')
    ):
        return (HTTPStatus.OK.value, {}, '')

    return (HTTPStatus.BAD_REQUEST, {}, '')

def test_authorized_login(auth, _response):
    auth.login('valid-email', 'valid-password')

def test_unauthorized_login(auth, _response):
    with pytest.raises(InvalidCredentials):
        auth.login('wrong-email', 'wrong-password')
