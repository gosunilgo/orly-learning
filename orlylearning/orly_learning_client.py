from .handler import AuthHandler, BookHandler, UserHandler

class ORlyLearningClient():

    def __init__(self, session=None, proxy=None):
        self.proxy = proxy

        self.auth_handler = AuthHandler(session, proxy)
        self.book_handler = BookHandler(session)
        self.user_handler = UserHandler(session)

    def login(self, email, password):
        self.set_session(self.auth_handler.login(email, password))

    def logout(self):
        self.set_session(self.auth_handler.logout(), set_proxy=False)

    def register(self, fields_dict):
        self.set_session(
            self.auth_handler.register(fields_dict), set_proxy=False
        )

    def get_user_info(self):
        return self.user_handler.get_info()

    def get_book_info(self, book_id):
        return self.book_handler.get_info(book_id)

    def get_book_chapters_info(self, book_id):
        return self.book_handler.get_chapters_info(book_id)

    def set_session(self, session, set_proxy=True):
        if session and set_proxy:
            session.proxies = self.proxy

        self.auth_handler.session = session
        self.book_handler.session = session
        self.user_handler.session = session

    def set_proxy(self, proxy):
        self.proxy = proxy

        self.auth_handler.proxy = self.proxy
        self.auth_handler.session.proxies = self.proxy
        self.book_handler.session.proxies = self.proxy
        self.user_handler.session.proxies = self.proxy
