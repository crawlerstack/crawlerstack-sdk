"""爬虫程序开启入口"""
import asyncio

from example.crawlers import DemoCrawlers

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DemoCrawlers().crawlers())
