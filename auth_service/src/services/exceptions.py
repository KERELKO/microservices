class AuthServiceException(Exception):
    ...


class NoPasswordException(AuthServiceException):
    ...


class NoUsernameException(AuthServiceException):
    ...
