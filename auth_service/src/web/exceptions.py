from fastapi import HTTPException, status


IncorrectCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'},
)
