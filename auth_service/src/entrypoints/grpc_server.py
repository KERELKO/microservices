from dataclasses import asdict

import uvloop

import grpc
import grpc.experimental
import grpc_.unary_auth_pb2_grpc as pb2_grpc
import grpc_.unary_auth_pb2 as pb2

from src.common.exceptions import IncorrectCredentialsException
from src.common.di import Container
from src.services import auth


class UnaryAuthService(pb2_grpc.AuthServiceServicer):
    async def GetUserByToken(
        self,
        request: pb2.RequestUser,
        context: grpc.aio.ServicerContext,
    ) -> pb2.Response:
        service = Container.resolve(auth.AuthService)
        errors = []
        meta = {}
        user = None
        try:
            _user = await service.get_user_by_token(request.token)
            user = pb2.User(**asdict(_user))
        except IncorrectCredentialsException:
            errors.append(IncorrectCredentialsException.__name__)
        response = pb2.Response(
            data=user,
            errors=errors,
            meta=meta
        )
        return response


async def start_service() -> None:
    server = grpc.aio.server()
    pb2_grpc.add_AuthServiceServicer_to_server(UnaryAuthService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


def main() -> None:
    uvloop.run(start_service())


if __name__ == '__main__':
    main()
