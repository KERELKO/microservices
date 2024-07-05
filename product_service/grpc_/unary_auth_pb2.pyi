from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestUser(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("data", "errors", "meta")
    class MetaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    data: User
    errors: _containers.RepeatedScalarFieldContainer[str]
    meta: _containers.ScalarMap[str, str]
    def __init__(self, data: _Optional[_Union[User, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ..., meta: _Optional[_Mapping[str, str]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "username", "email")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    email: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...
