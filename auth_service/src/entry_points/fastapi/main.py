from fastapi import FastAPI

from .handlers import router as auth_router


def app_factory() -> FastAPI:
    app = FastAPI(docs_url='/api/docs')

    app.include_router(auth_router)

    return app
