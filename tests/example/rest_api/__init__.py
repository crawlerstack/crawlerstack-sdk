"""rest api"""
from example.rest_api.api import router
from fastapi import FastAPI


def init_app():
    """
    api v1
    :return:
    """
    app = FastAPI()
    app.include_router(router, prefix='/api/v1')

    return app
