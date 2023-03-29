"""
模拟一个采集平台 api
并在示例爬虫执行前，开启 api server
"""
import asyncio
import signal as system_signal

from example.rest_api import init_app
from uvicorn import Config, Server
from uvicorn.server import HANDLED_SIGNALS


class ServerManager:
    """server manager"""

    def __init__(self):
        self.uvicorn_config = Config(init_app(), host='0.0.0.0')
        self.uvicorn_server = Server(self.uvicorn_config)
        self.should_exit = False
        self.force_exit = True

    async def uvicorn_server_setup(self):
        """uvicorn server setup"""
        config = self.uvicorn_server.config
        if not config.loaded:
            config.load()

        self.uvicorn_server.lifespan = config.lifespan_class(config)
        await self.uvicorn_server.startup()

    async def stop(self) -> None:
        """stop"""
        # 由于 _uvicorn_server 是在 startup 是初始化 servers 属性的，
        # 所以在测试时，如果不运行 self.start 逻辑， _uvicorn_server.shutdown
        # 会报错
        if hasattr(self.uvicorn_server, 'servers'):
            await self.uvicorn_server.shutdown()

    async def start(self):
        """start"""
        try:
            self.install_signal_handlers()
            await self.uvicorn_server_setup()
            while not self.should_exit:
                await asyncio.sleep(0.01)
        except Exception:  # pylint: disable=broad-exception-caught
            pass
        finally:
            await asyncio.sleep(0.01)
            await self.stop()

    def install_signal_handlers(self) -> None:
        """
        覆盖信号处理函数，捕获 Ctrl-C 信号，以便于优雅处理强制结束逻辑。

        :return:
        """
        loop = asyncio.get_event_loop()

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, self.handle_exit, sig, None)
        except NotImplementedError:  # pragma: no cover
            # Windows
            for sig in HANDLED_SIGNALS:
                system_signal.signal(sig, self.handle_exit)

    def handle_exit(self, _sig, _frame):
        """
        处理退出逻辑。

        :param _sig:
        :param _frame:
        :return:
        """
        if self.should_exit:
            self.force_exit = True
        else:
            self.should_exit = True


if __name__ == '__main__':
    asyncio.run(ServerManager().start())
