from src.dto import UserDTO


def register_user(user_data: UserDTO):
    ...


def login(user_data: UserDTO):
    ...


def logout(user_data: UserDTO):
    ...


def login_by_token(token: str):
    ...


def update_token(user_data: UserDTO):
    ...
