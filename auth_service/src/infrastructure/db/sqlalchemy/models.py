from sqlalchemy import Integer, Table, Column, String
from sqlalchemy.orm import registry

from src.domain.storage import StoredUser


mapper_registry = registry()

user_table = Table(
    'users',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('email', String(50), nullable=True),
    Column('hashed_password', String(300), nullable=True),
)


mapper_registry.map_imperatively(StoredUser, user_table)
