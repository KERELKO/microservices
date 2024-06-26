from dataclasses import asdict

from fastapi import APIRouter

from src.dto import schemas, domain
from src.services import AuthService


router = APIRouter(prefix='/auth')


@router.post('/register', response_model=schemas.UserOut)
async def register_user(user_in: schemas.UserIn) -> schemas.UserOut:
    service = AuthService()
    dto = domain.UserDTO(**user_in.model_dump())
    dto_read = await service.register_user(dto)
    return schemas.UserOut(**asdict(dto_read))


@router.post('/login', response_model=str)
async def login(username: str, password: str) -> str:
    ...
