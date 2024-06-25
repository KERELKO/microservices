from src.dto.domain import UserDTO, UserSecureDTO, UserReadDTO
from src.storages.repositories.impl import UserRepository
from src.exceptions import raise_exc
from src.utils import hash_password


class AuthService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    async def register_user(self, dto: UserDTO) -> UserReadDTO:
        password = dto.password if dto.password else raise_exc(
            Exception('Password was not provided'),
        )
        user = UserSecureDTO(
            username=dto.username,
            hashed_password=hash_password(password),
            email=dto.email,
        )
        new_user = await self.repository.add(user)
        return new_user

    async def login(self, username: str, password: str) -> UserReadDTO:
        hashed_password = hash_password(password)
        dto = await self.repository.get_by_username(username)
        user = dto if dto is not None else raise_exc(
            exc=Exception(f'User with username "{username}" not found')
        )
        if hashed_password != user.hashed_password:
            raise Exception('Passwords didn\'t match')
        return UserReadDTO(username=user.username, id=user.id, email=user.email)

    async def logout(self, dto: UserDTO):
        ...

    async def login_by_token(self, token: str):
        ...

    async def update_token(self, dto: UserDTO):
        ...
