class LoginFailedException(Exception):
    def __init__(self, user, message='Login failed for user '):
        self.user = user
        self.message = f"{message} {self.user}\n"