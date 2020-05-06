import json
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urljoin, urlparse, quote_plus

from requests import Session
from requests.exceptions import RequestException

from .auth import Auth
from .book import Book
from .constants.urls import Url

class OReillyLearningClient():

    def __init__(self, session=None, proxy=None):
        self.proxy = proxy

        self.auth = Auth(session, proxy)
        self.book = Book(session)

    def login(self, email, password):
        self.set_session(self.auth.login(email, password))

    def logout(self):
        self.set_session(self.auth.logout(), set_proxy=False)

    def register(self, fields_dict):
        self.set_session(self.auth.register(fields_dict), set_proxy=False)

    def get_book_info(self, book_id):
        return self.book.get_info(book_id)

    def get_book_chapters_info(self, book_id):
        return self.book.get_chapters_info(book_id)

    def set_session(self, session, set_proxy=True):
        if session and set_proxy:
            session.proxies = self.proxy

        self.auth.session = session
        self.book.session = session

    def set_proxy(self, proxy):
        self.proxy = proxy

        self.auth.proxy = self.proxy
        self.auth.session.proxies = self.proxy
        self.book.session.proxies = self.proxy
