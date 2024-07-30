class DomainException(Exception):
    ...


class IncorrectCredentialsException(DomainException):
    ...


class FailToAuthorizeException(DomainException):
    ...
