from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str
    email: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
