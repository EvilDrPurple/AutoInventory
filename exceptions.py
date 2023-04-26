class LoginFailedError(Exception):
    def __init__(self, user, message='Login failed for user'):
        self.user = user
        self.message = f"{message} {self.user}"


class UserCancelled(Exception):
    def __init__(self, message='Process cancelled by user'):
        self.message = message


class SaveFailedError(Exception):
    def __init__(self, message='\nSaving inventory sheet failed'):
        self.message = message