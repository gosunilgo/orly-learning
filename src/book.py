from urllib.parse import urljoin

from .constants.urls import Url
from .exceptions import InvalidSession

class Book():
    
    LEARNING_BOOK = urljoin(Url.LEARNING, '/api/v1/book/{}/')
    LEARNING_BOOK_CHAPTER = urljoin(LEARNING_BOOK, 'chapter/')
    
    def __init__(self, session):
        self.session = session
    
    def get_info(self, book_id):
        if not self.session:
            raise InvalidSession()

        return self.session.get(Book.LEARNING_BOOK.format(book_id)).json()
    
    def get_chapters_info(self, book_id):
        if not self.session:
            raise InvalidSession()

        return [
            chapter
            for page_chapters in self.__get_chapters(
                Book.LEARNING_BOOK_CHAPTER.format(book_id)
            )
            for chapter in page_chapters
        ]

    def __get_chapters(self, page_url):
        response = self.session.get(page_url).json()
        yield response['results']
        if response['next']:
            yield from self.__get_chapters(response['next'])
        