class LoginFailedError(Exception):
    def __init__(self, user, message='Login failed for user '):
        self.user = user
        self.message = f"{message} {self.user}\n"

class UserCancelled(Exception):
    def __init__(self, message='Process cancelled by user\n'):
        self.message = message