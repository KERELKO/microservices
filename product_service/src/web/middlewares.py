from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from fastapi.responses import HTMLResponse
from fastapi import Request

from pyinstrument import Profiler


class PyinstrumentProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        profiling = request.query_params.get('profile', False)
        if profiling:
            profiler = Profiler(async_mode='enabled')
            profiler.start()
            await call_next(request)
            profiler.stop()
            return HTMLResponse(profiler.output_html())
        else:
            return await call_next(request)
