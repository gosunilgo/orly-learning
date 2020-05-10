class EmailError(Exception):
    pass

class PasswordError(Exception):
    pass

class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__('email or password are incorrect')

class InvalidSession(Exception):
    def __init__(self):
        super().__init__('the provided session is not valid')
