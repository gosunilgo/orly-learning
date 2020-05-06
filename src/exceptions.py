class EmailError(Exception):
    pass

class PasswordError(Exception):
    pass

class InvalidSession(Exception):
    def __init__(self):
        super().__init__('the provided session is not valid')