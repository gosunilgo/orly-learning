from http import HTTPStatus

import pytest
import responses

from orlylearning.exceptions import InvalidCredentials
from orlylearning.handler import AuthHandler

@pytest.fixture(name='auth')
def init_auth():
    return AuthHandler(None, None)

@responses.activate
def test_authorized_login(auth):
    responses.add(
        responses.POST, AuthHandler.OREILLY_LOGIN, status=HTTPStatus.OK.value
    )
    auth.login('email', 'password')

@responses.activate
def test_unauthorized_login(auth):
    responses.add(
        responses.POST,
        AuthHandler.OREILLY_LOGIN,
        status=HTTPStatus.BAD_REQUEST.value
    )
    with pytest.raises(InvalidCredentials):
        auth.login('wrong.email', 'wrong-password')
