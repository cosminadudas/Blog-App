class LoginError(BaseException):
    pass

class UserNotSetupError(BaseException):
    pass

class UserAlreadyExists(BaseException):
    pass

class FormatFileNotAccepted(BaseException):
    pass
