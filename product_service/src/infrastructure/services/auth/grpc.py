import grpc.experimental  # type: ignore[import-untyped]
import grpc
import grpc_.unary_auth_pb2_grpc as pb2_grpc
import grpc_.unary_auth_pb2 as pb2

from src.common.config import get_conf
from src.infrastructure.dto.auth import User

from .base import AbstractAuthService, AuthServiceException


class GRPCAuthService(AbstractAuthService[User]):
    def __init__(self, url: str | None = None) -> None:
        self.conf = get_conf()
        self.url = url or self.conf.grpc_uri

    async def get_user_by_token(self, token: str) -> User:
        async with grpc.aio.insecure_channel(self.url) as channel:
            stub = pb2_grpc.AuthServiceStub(channel)
            response: pb2.Response = await stub.GetUserByToken(pb2.RequestUser(token=token))
            data = response.data

        if not response.errors and data:
            _user: pb2.User = data
            user = User(id=str(_user.id), username=_user.username, email=_user.email)
            return user

        raise AuthServiceException('Failed to process the response', response.errors, self.url)
