from http import HTTPStatus
from http.cookies import SimpleCookie
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response, Session
from requests.exceptions import RequestException

from ..constants.headers import Headers
from ..constants.urls import Url
from ..exceptions import EmailError, PasswordError, InvalidCredentials

from .abstract_handler import AbstractHandler

class AuthHandler(AbstractHandler):

    OREILLY_LOGIN = urljoin(Url.OREILLY, 'member/auth/login/')
    LEARNING_LOGOUT = urljoin(Url.LEARNING, 'accounts/logout/')
    API_END_SESSION = urljoin(Url.API, 'v1/auth/openid/end-session/')
    LEARNING_REGISTER = urljoin(Url.LEARNING, 'register/')
    LEARNING_EMAIL_CHECK = urljoin(Url.LEARNING, 'check-email-availability/')
    LEARNING_PASSWORD_CHECK = urljoin(Url.LEARNING, 'check-password/')

    def __init__(self, session: Session, proxy: dict):
        super().__init__(session)
        self.proxy = proxy

    def login(self, email: str, password: str) -> Session:
        self.__initialize_session()
        self.session.headers.update({'Referer': Url.LEARNING})

        login_post_response = self.session.post(
            AuthHandler.OREILLY_LOGIN,
            json={
                'email': email,
                'password': password
            }
        )

        if login_post_response.status_code == HTTPStatus.BAD_REQUEST.value:
            raise InvalidCredentials()

        self.__handle_broken_cookies(login_post_response)

        return self.session

    def logout(self):
        self.session.get(AuthHandler.LEARNING_LOGOUT)
        self.session.get(AuthHandler.API_END_SESSION)
        self.session = None

        return self.session

    def register(self, fields: dict):
        self.__initialize_session()
        self.session.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': AuthHandler.LEARNING_REGISTER
        })

        register_get_response = BeautifulSoup(
            self.session.get(AuthHandler.LEARNING_REGISTER).text, 'lxml'
        )

        email_check_response = self.session.get(
            AuthHandler.LEARNING_EMAIL_CHECK, params={'email': fields['email']}
        ).json()

        if not email_check_response['success']:
            raise EmailError(email_check_response['message'])

        password_name = register_get_response.find(
            'input', {'type': 'password'}
        )['name']

        csrf_token = register_get_response.find(
            'input', {'name': 'csrfmiddlewaretoken'}
        )['value']

        password_check_response = self.session.post(
            AuthHandler.LEARNING_PASSWORD_CHECK,
            data={
                'csrfmiddlewaretoken': csrf_token,
                password_name: fields['password'],
                'field_name': password_name
            }
        ).json()

        if not password_check_response['valid']:
            raise PasswordError(password_check_response['msg'])

        register_post_response = self.session.post(
            AuthHandler.LEARNING_REGISTER,
            data={
                'next': '',
                'trial_length': register_get_response.find(
                    id='id_trial_length'
                )['value'],
                'csrfmiddlewaretoken': csrf_token,
                'first_name': fields['first_name'],
                'last_name': fields['last_name'],
                'email': fields['email'],
                'password1': fields['password'],
                'country': fields['country'],
                'referrer': fields['referrer'],
                'recently_viewed_bits': '[]'
            }
        )

        self.__handle_broken_cookies(register_post_response)

        return self.session

    def __handle_broken_cookies(self, response: Response):
        for cookie in response.raw.headers.getlist('Set-Cookie'):
            simple_cookie = SimpleCookie()
            simple_cookie.load(cookie)
            for key, morsel in simple_cookie.items():
                try:
                    int(morsel['max-age'])
                except ValueError:
                    self.session.cookies.set(key, morsel.value)

    def __initialize_session(self):
        self.session = Session()

        if self.proxy:
            self.session.proxies = self.proxy
            self.session.verify = False

        self.session.headers.update(Headers.HEADERS)
