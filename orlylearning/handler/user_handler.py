from http import HTTPStatus
import json
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup, SoupStrainer

from ..constants.urls import Url
from ..exceptions import InvalidSession

from .abstract_handler import AbstractHandler

class UserHandler(AbstractHandler):

    LEARNING_PROFILE = urljoin(Url.LEARNING, 'profile/')

    INITIAL_STORE_DATA_SEARCH = 'window.initialStoreData = '
    INITIAL_STORE_DATA__VALUE_REGEX = re.compile(
        r"window\.initialStoreData = (.+?);", re.S
    )

    def get_info(self):
        self._check_session()

        response = self.session.get(
            UserHandler.LEARNING_PROFILE, allow_redirects=False
        )
        if response.status_code != HTTPStatus.OK.value:
            raise InvalidSession()
        scripts = BeautifulSoup(
            response.text, 'lxml', parse_only=SoupStrainer('head')
        ).find_all('script')
        for script in scripts:
            if (
                    script.string
                    and UserHandler.INITIAL_STORE_DATA_SEARCH in script.string
            ):
                return json.loads(
                    UserHandler.INITIAL_STORE_DATA__VALUE_REGEX.findall(
                        script.string
                    )[0]
                ).get('user')
