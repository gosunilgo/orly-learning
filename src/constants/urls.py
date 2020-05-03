from enum import Enum

from urllib.parse import urljoin

class Url(Enum):
    _ignore_ = "SCHEME, OREILLY_BASE_HOST"

    SCHEME = 'https://'
    OREILLY_BASE_HOST = 'oreilly.com'

    API = '{}api.{}'.format(SCHEME, OREILLY_BASE_HOST)
    OREILLY = '{}www.{}'.format(SCHEME, OREILLY_BASE_HOST)
    LEARNING = '{}learning.{}'.format(SCHEME, OREILLY_BASE_HOST)
    LEARNING_PROFILE = urljoin(LEARNING, 'profile')

    def __str__(self):
        return self.value
