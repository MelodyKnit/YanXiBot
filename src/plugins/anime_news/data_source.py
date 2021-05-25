from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .config import Config
from datetime import datetime

config = Config()


async def get(url, headers):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as reply:
            return BeautifulSoup(await reply.read(), features="html.parser")


async def anime_news():
    values = ["今日最新新番更新动态"]
    html = await get(config.main_url, config.headers)
    for li in html.select("div.tlist > ul")[datetime.now().weekday()].select("li"):
        a = li.select("a")
        values.append(f"番名: {a[1].text}\n更新至{a[0].text}")
    return "\n".join(values)
