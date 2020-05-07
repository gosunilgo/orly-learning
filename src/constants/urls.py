class Url():

    __SCHEME = 'https://'
    __OREILLY_BASE_HOST = 'oreilly.com'

    API = '{}api.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
    OREILLY = '{}www.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
    LEARNING = '{}learning.{}'.format(__SCHEME, __OREILLY_BASE_HOST)
