"""server start"""
from example.rest_api import init_app
from uvicorn import Config, Server

uvicorn_config = Config(init_app(), host='0.0.0.0')
uvicorn_server = Server(uvicorn_config)


async def uvicorn_server_setup():
    """uvicorn server setup"""
    config = uvicorn_server.config
    if not config.loaded:
        config.load()

    uvicorn_server.lifespan = config.lifespan_class(config)
    await uvicorn_server.startup()


async def stop() -> None:
    """stop"""
    # 由于 _uvicorn_server 是在 startup 是初始化 servers 属性的，
    # 所以在测试时，如果不运行 self.start 逻辑， _uvicorn_server.shutdown
    # 会报错
    if hasattr(uvicorn_server, 'servers'):
        await uvicorn_server.shutdown()
