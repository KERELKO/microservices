from dataclasses import asdict
from typing import Annotated
from fastapi import Cookie, HTTPException, status

from src.common.container import Container
from src.services.base import AbstractAuthService
from src.web.schemas import UserOut


async def get_current_user(token: Annotated[str | None, Cookie()] = None) -> UserOut:
    """
    Tries to get user from token located in `Cookies`

    if not token, or token is invalid raises `HTTPException(401)`
    """
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    service: AbstractAuthService = Container.resolve(AbstractAuthService)
    try:
        user = await service.get_user_by_token(token=token)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return UserOut(**asdict(user))
