from fastapi import FastAPI
from src.handlers import router as product_router


def app_factory():
    app = FastAPI()
    app.include_router(product_router)

    return app
