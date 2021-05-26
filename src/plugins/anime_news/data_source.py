from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .config import Config
from datetime import datetime

config = Config()


async def get(url, headers):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as reply:
            return BeautifulSoup(await reply.read(), features="html.parser")


class AnimeNews:
    def __init__(self):
        self.html = None

    def __await__(self):
        return self.get_html().__await__()

    async def get_html(self):
        self.html = await get(config.main_url, config.headers)
        return self

    def ranking(self):
        values = ["一周动漫排行榜"]
        for li in self.html.select("div.pics > ul > li"):
            span = li.select("span")
            values.append(f"番名：{li.find('h2').text}"
                          f"\n{span[0].text}\n" +
                          span[1].text.replace('\t', "").replace("\n", " "))
        return "\n---\n".join(values)

    def update(self):
        values = [f"早上好，今天是{datetime.today().date()}", "为您报道最新新番更新动态"]
        for li in self.html.select("div.tlist > ul")[datetime.now().weekday()].select("li"):
            a = li.select("a")
            values.append(f"-番名: {a[1].text}\n-更新至{a[0].text}")
        return "\n---\n".join(values)
