from dataclasses import asdict
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.dto.domain import UserDTO
from src.services import AuthService
from src.dto.schemas import Token, UserIn, UserOut
from src.config import config
from src import exceptions

from .exceptions import IncorrectCredentialsException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
router = APIRouter(prefix='/auth')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    service = AuthService()
    try:
        user = await service.get_user_by_token(token=token)
    except exceptions.IncorrectCredentialsException:
        raise IncorrectCredentialsException
    return user


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    service = AuthService()
    user = await service.authenticate_user(form_data.username, form_data.password)
    if user is False:
        raise IncorrectCredentialsException
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires,  # type: ignore
    )
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me/', response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)],
) -> UserOut:
    return current_user


@router.post('/register', response_model=UserOut)
async def register_user(user_data: UserIn) -> UserOut:
    service = AuthService()
    dto = UserDTO(**user_data.model_dump())
    new_user = await service.register_user(dto)
    return UserOut(**asdict(new_user))
