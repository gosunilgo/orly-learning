from urllib.parse import urljoin

class Url():

    __SCHEME = 'https://'
    __OREILLY_BASE_HOST = 'oreilly.com'

    API = '{}api.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
    OREILLY = '{}www.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
    LEARNING = '{}learning.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
    LEARNING_PROFILE = urljoin(LEARNING, 'profile/')
    LEARNING_BOOK = urljoin(LEARNING, '/api/v1/book/')
