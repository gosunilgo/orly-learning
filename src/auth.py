from http.cookies import SimpleCookie
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import RequestException

from src.constants.headers import Headers
from src.constants.urls import Url

from .exceptions import EmailError, PasswordError

class Auth():

    OREILLY_LOGIN = urljoin(Url.OREILLY, 'member/auth/login/')
    LEARNING_REGISTER = urljoin(Url.LEARNING, 'register/')
    LEARNING_EMAIL_CHECK = urljoin(Url.LEARNING, 'check-email-availability/')
    LEARNING_PASSWORD_CHECK = urljoin(Url.LEARNING, 'check-password/')

    def __init__(self, proxy):
        self.proxy = proxy
    
    def login(self, email, password):
        session = self.__initialize_session()
        session.headers.update({'Referer': Url.LEARNING})

        try:
            login_post_response = session.post(
                Auth.OREILLY_LOGIN,
                json={
                    'email': email,
                    'password': password
                }
            )
            
            self.__handle_broken_cookies(login_post_response, session)

            return session
        except RequestException:
            return None
    
    def register(self, fields):
        session = self.__initialize_session()
        session.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': Auth.LEARNING_REGISTER
        })

        register_get_response = BeautifulSoup(
            session.get(Auth.LEARNING_REGISTER).text,
            'html.parser'
        )

        email_check_response = session.get(
            Auth.LEARNING_EMAIL_CHECK, params={'email': fields['email']}
        ).json()

        if not email_check_response['success']:
            raise EmailError(email_check_response['message'])

        password_name = register_get_response.find(
            'input', {'type': 'password'}
        )['name']

        csrf_token = register_get_response.find(
            'input', {'name': 'csrfmiddlewaretoken'}
        )['value']

        password_check_response = session.post(
            Auth.LEARNING_PASSWORD_CHECK,
            data={
                'csrfmiddlewaretoken': csrf_token,
                password_name: fields['password'],
                'field_name': password_name
            }
        ).json()

        if not password_check_response['valid']:
            raise PasswordError(password_check_response['msg'])

        register_post_response = session.post(
            Auth.LEARNING_REGISTER,
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

        self.__handle_broken_cookies(register_post_response, session)
    
        return session

    def __handle_broken_cookies(self, response, session):
        for cookie in response.raw.headers.getlist('Set-Cookie'):
            simple_cookie = SimpleCookie()
            simple_cookie.load(cookie)
            for key, morsel in simple_cookie.items():
                try:
                    int(morsel['max-age'])
                except ValueError:
                    session.cookies.set(key, morsel.value)

    def __initialize_session(self):
        session = Session()

        if self.proxy:
            session.proxies = self.proxy
            session.verify = False
        
        session.headers.update(Headers.HEADERS)

        return session
