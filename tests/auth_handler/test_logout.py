from http import HTTPStatus

from pytest import fixture, raises
import responses
from requests import Session

from orlylearning.exceptions import InvalidSession
from orlylearning.handler import AuthHandler

@fixture(name='invalid_session_auth', params=[None, Session()])
def init_invalid_auth(request):
    return AuthHandler(request.param, None)

@fixture(name='auth')
def init_auth():
    return AuthHandler(None, None)

@responses.activate
def test_invalid_logout(invalid_session_auth):
    responses.add(
        responses.GET,
        AuthHandler.LEARNING_LOGOUT,
        status=HTTPStatus.OK.value
    )
    responses.add(
        responses.GET,
        AuthHandler.API_END_SESSION,
        status=HTTPStatus.FORBIDDEN.value
    )
    with raises(InvalidSession):
        invalid_session_auth.logout()
