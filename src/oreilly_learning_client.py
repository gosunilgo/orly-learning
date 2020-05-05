import json
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urljoin, urlparse, quote_plus

from requests import Session
from requests.exceptions import RequestException

from .constants.urls import Url

from .auth import Auth

class OReillyLearningClient():

    def __init__(self, session=None, proxy=None):
        self.session = session
        self.proxy = proxy

    def login(self, email, password):
        self.session = Auth(self.proxy).login(email, password)
        return bool(self.session)

    def register(self, fields_dict):
        self.session = Auth(self.proxy).register(fields_dict)
        return bool(self.session)
    
    def get_book_info(self, book_id):
        return self.session.get(
            '{}{}/'.format(Url.LEARNING_BOOK, book_id)
        ).json()
        
