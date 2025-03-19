from uuid import uuid4

from src.infrastructure.dto.auth import User

from .base import AbstractAuthService


class FakeAuthService(AbstractAuthService[User]):
    async def get_user_by_token(self, token: str) -> User:
        return User(id=f'{uuid4()}', username=f'test-user-token:{token}', email='test@user.com')
