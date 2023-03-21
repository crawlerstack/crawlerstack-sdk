"""rest api"""
from example.rest_api.api import router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def init_app():
    """
    api v1
    :return:
    """
    app = FastAPI()
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    app.include_router(router, prefix='/api/v1')

    return app
