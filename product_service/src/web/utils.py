from dataclasses import asdict
from typing import Annotated

from fastapi import HTTPException, status, Header

from src.services.base import AbstractAuthService
from src.services.exceptions import AuthServiceException
from src.web.schemas import UserOut

from . import ContainerDep


async def get_current_user(
    container: ContainerDep,
    auth: Annotated[str, Header(alias='Authorization')] = '',
) -> UserOut:
    """
    Tries to get user from token located in `Authorization header`

    if not token, or token is invalid raises `HTTPException(401)`
    """
    print(auth)
    if not auth or len(splt := auth.split()) != 2:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    _, token = splt
    service = container.resolve(AbstractAuthService)  # type: ignore
    try:
        user = await service.get_user_by_token(token=token)
    except AuthServiceException as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return UserOut(**asdict(user))
