class DomainException(Exception):
    ...


class UserDoesNotExist(Exception):
    ...


class IncorrectCredentialsException(DomainException):
    ...


class FailedToAuthorizeException(DomainException):
    ...


class AuthServiceException(Exception):
    ...


class NoPasswordException(AuthServiceException):
    ...


class NoUsernameException(AuthServiceException):
    ...


class UsernameAlreadyTaken(AuthServiceException):
    ...
