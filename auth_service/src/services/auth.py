from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.common.config import get_conf
from src.common.dto import UserInputDTO, UserReadDTO, UserSecureDTO
from src.common.exceptions import FailToAuthorizeException, IncorrectCredentialsException
from src.common.utils import raise_exc
from src.storages.repositories.base import AbstractUserRepository

from .exceptions import NoPasswordException, NoUsernameException


class AuthService:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self.repo = repository
        self.conf = get_conf()
        self.pwd_context = self.conf.CRYPTO_CONTEXT

    async def get_user(self, username: str) -> UserReadDTO | None:
        user = await self.repo.get_by_username(username=username)
        return self._safe_user(user) if user else None

    async def get_user_by_token(self, token: str) -> UserReadDTO:
        """Returns a user or raises `IncorrectCredentialsException`"""
        try:
            payload = jwt.decode(token, self.conf.SECRET_KEY, algorithms=[self.conf.ALGORITHM])
            username: str | None = payload.get('sub', None)
            if not username:
                raise IncorrectCredentialsException
        except jwt.InvalidTokenError:
            raise IncorrectCredentialsException
        user = await self.get_user(username=username)
        return user if user else raise_exc(IncorrectCredentialsException())

    async def register_user(self, dto: UserInputDTO) -> UserReadDTO:
        password = dto.password if dto.password else raise_exc(NoPasswordException())
        username = dto.username if dto.username else raise_exc(NoUsernameException())
        user = UserSecureDTO(
            username=username,
            hashed_password=self.get_password_hash(password),
            email=dto.email,
        )
        new_user = await self.repo.add(user)
        return self._safe_user(new_user)

    def _safe_user(self, user_secure: UserSecureDTO) -> UserReadDTO:
        user_data = asdict(user_secure)
        if 'password' in user_data:
            user_data.pop('password')
        if 'hashed_password' in user_data:
            user_data.pop('hashed_password')
        return UserReadDTO(**user_data)

    async def authenticate_user(self, username: str, password: str) -> UserReadDTO:
        user: UserSecureDTO | None = await self.repo.get_by_username(username=username)
        if not user or not self.verify_password(password, user.hashed_password):
            raise FailToAuthorizeException
        return self._safe_user(user)

    async def login(self, username: str, password: str) -> str:
        try:
            user: UserReadDTO | bool = await self.authenticate_user(username, password)
        except FailToAuthorizeException:
            raise IncorrectCredentialsException
        access_token_expires = timedelta(minutes=self.conf.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={'sub': user.username}, expires_delta=access_token_expires,
        )
        return access_token

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(
        self,
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.conf.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.conf.SECRET_KEY, algorithm=self.conf.ALGORITHM)
        return encoded_jwt
