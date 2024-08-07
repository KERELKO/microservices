from fastapi import FastAPI

from src.web.handlers import router as product_router
from src.web.middlewares import PyinstrumentProfilerMiddleware

from src.common.config import get_conf


def app_factory() -> FastAPI:
    config = get_conf()

    app = FastAPI(docs_url='/api/docs')
    app.include_router(prefix='/api', router=product_router)

    if config.PROFILING:
        app.add_middleware(PyinstrumentProfilerMiddleware)
    return app
