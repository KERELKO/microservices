from fastapi import FastAPI

from src.web.handlers import router as product_router


def app_factory() -> FastAPI:
    app = FastAPI(docs_url='/api/docs')
    app.include_router(product_router)

    return app
