from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.common.di import Container, build_container
from src.domain.service import AuthService, RegisterUserDTO
from .schemas import Token, UserIn, UserOut
from src.domain.exceptions import IncorrectCredentialsException, AuthServiceException


ContainerDep = Annotated[Container, Depends(build_container)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')
router = APIRouter(prefix='/api/v1/auth')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    container: ContainerDep,
):
    service = container.resolve(AuthService)
    try:
        user = await service.get_user_by_token(token=token)
    except IncorrectCredentialsException:
        raise IncorrectCredentialsException
    return user


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    container: ContainerDep,
) -> Token:
    service = container.resolve(AuthService)
    try:
        access_token = await service.login(form_data.username, form_data.password)
    except IncorrectCredentialsException:
        raise IncorrectCredentialsException
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me/', response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)],
) -> UserOut:
    return current_user


@router.post('/register', response_model=UserOut)
async def register_user(
    user_data: UserIn,
    container: ContainerDep,
) -> UserOut:
    service = container.resolve(AuthService)
    dto = RegisterUserDTO(**user_data.model_dump())
    try:
        new_user_id = await service.register_user(dto)
    except AuthServiceException as e:
        raise HTTPException(status_code=400, detail=str(e))
    user_out = UserOut(**asdict(dto), id=new_user_id)
    return user_out
