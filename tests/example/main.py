"""main"""
import asyncio

from example.crawlers import DemoCrawlers
from example.rest_api.server_start import stop, uvicorn_server_setup


async def start():
    """Start"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await uvicorn_server_setup()
    await asyncio.sleep(2)
    await DemoCrawlers().crawlers()
    await asyncio.sleep(2)
    await stop()
    await asyncio.sleep(5)
    loop.close()


if __name__ == '__main__':
    asyncio.run(start())
