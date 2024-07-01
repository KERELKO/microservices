from typing import Any
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.config import config
from src.dto.domain import UserDTO, UserSecureDTO, UserReadDTO
from src.storages.repositories.impl import UserRepository
from src.exceptions import raise_exc, IncorrectCredentialsException
from src.utils import hash_password


class AuthService:
    def __init__(self) -> None:
        self.repository = UserRepository()
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def get_user(self, username: str) -> UserSecureDTO | None:
        return await self.repository.get_by_username(username=username)

    async def get_user_by_token(self, token: str) -> UserSecureDTO:
        """Returns a user or raises `IncorrectCredentialsException` exception"""
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise IncorrectCredentialsException
        except jwt.InvalidTokenError:
            raise IncorrectCredentialsException
        user = await self.get_user(username=username)
        return user if user else raise_exc(IncorrectCredentialsException())

    async def register_user(self, dto: UserDTO) -> UserReadDTO:
        password = dto.password if dto.password else raise_exc(
            Exception('Password was not provided'),
        )
        username = dto.username if dto.username else raise_exc(
            Exception('Username was not provided'),
        )
        user = UserSecureDTO(
            username=username,
            hashed_password=hash_password(password),
            email=dto.email,
        )
        new_user = await self.repository.add(user)
        return new_user

    async def authenticate_user(self, username: str, password: str) -> UserSecureDTO | bool:
        user: UserSecureDTO | None = await self.repository.get_by_username(username=username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def login(self, username: str, password: str) -> str:
        user: UserSecureDTO | bool = await self.authenticate_user(username, password)
        if user is False:
            raise IncorrectCredentialsException
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={'sub': user.username}, expires_delta=access_token_expires,  # type: ignore
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
                minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt
