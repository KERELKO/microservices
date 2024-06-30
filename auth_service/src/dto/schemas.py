from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str
    password: str
    email: str = Field(default='')


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = Field(default='')
