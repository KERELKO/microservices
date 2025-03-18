from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.common.utils import raise_exc

from .entities import ID, User
from .exceptions import (FailedToAuthorizeException,
                         IncorrectCredentialsException, NoPasswordException,
                         NoUsernameException, UserDoesNotExist, UsernameAlreadyTaken)
from .storage import StoredUser, UserStorage


@dataclass
class RegisterUserDTO:
    username: str
    email: str | None = None
    password: str | None = None


type Token = str


class AuthService:
    def __init__(
        self,
        storage: UserStorage,
        crypto_context,
        access_token_expire_minutes: int,
        secret_key: str,
        algorithm: str,
    ) -> None:
        self.storage = storage
        self.crypto_context = crypto_context
        self.access_token_expire_minutes = access_token_expire_minutes
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def get_user_by_token(self, token: str) -> User:
        """Returns a user or raises `IncorrectCredentialsException`"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str | None = payload.get('sub', None)
            if not username:
                raise IncorrectCredentialsException
        except jwt.InvalidTokenError:
            raise IncorrectCredentialsException
        user = await self.storage.get_by_username(username=username)
        return user.as_user() if user else raise_exc(IncorrectCredentialsException())

    async def register_user(self, dto: RegisterUserDTO) -> ID:
        password = dto.password if dto.password else raise_exc(NoPasswordException())
        username = dto.username if dto.username else raise_exc(NoUsernameException())
        same_username = await self.storage.get_by_username(dto.username)
        if same_username is not None:
            raise UsernameAlreadyTaken
        stored_user = StoredUser(
            id=-1,
            username=username,
            hashed_password=self.get_password_hash(password),
            email=dto.email,
        )
        user_id = await self.storage.add(stored_user)
        return user_id

    async def authenticate_user(self, username: str, password: str) -> User:
        user: StoredUser | None = await self.storage.get_by_username(username=username)
        if not user:
            raise UserDoesNotExist(username)
        if not user.hashed_password:
            raise FailedToAuthorizeException('Invalid data')
        if self.verify_password(password, user.hashed_password) is False:
            raise FailedToAuthorizeException("Passwords didn't match")
        return user.as_user()

    async def login(self, username: str, password: str) -> Token:
        try:
            user: User = await self.authenticate_user(username, password)
        except FailedToAuthorizeException:
            raise IncorrectCredentialsException
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={'sub': user.username}, expires_delta=access_token_expires,
        )
        return access_token

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypto_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.crypto_context.hash(password)

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
                minutes=self.access_token_expire_minutes,
            )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
