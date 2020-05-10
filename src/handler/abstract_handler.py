from abc import ABC

from ..exceptions import InvalidSession

class AbstractHandler(ABC):
    def __init__(self, session):
        self.session = session

    def _check_session(self):
        if not self.session:
            raise InvalidSession()
