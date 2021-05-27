from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .config import Config
from datetime import datetime
from nonebot import require, get_driver
from typing import Optional, Union
readfile = require("readfile")
read_data = readfile.read_data
write_data = readfile.write_data

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


class Recipient:
    __slots__ = ("groups", "users", "recipient")

    def __init__(self):
        self.users: Optional[list] = None
        self.groups: Optional[list] = None
        self.recipient: Optional[dict] = None

    def __await__(self):
        return self.read_recipient().__await__()

    async def read_recipient(self):
        """基于引用值特性，通过更改recipient来同时改动self.users与groups"""
        self.recipient = await read_data(config.news_recipient_filename)
        self.users = self.recipient["users"]
        self.groups = self.recipient["groups"]
        return self

    async def _save(self):
        await write_data(config.news_recipient_filename, self.recipient)

    async def _add(self, __type: str, arg_id: Union[int, list]) -> bool:
        if arg_id:
            add_to_id = set(self.recipient[__type])
            arg_id = {arg_id} if isinstance(arg_id, int) else set(arg_id)
            # 是否存在差集
            if arg_id - add_to_id:
                # 取出两者并集
                self.recipient[__type] = list(add_to_id | arg_id)
                await self._save()
                return True
        return False

    async def _remove(self, __type: str, arg_id: Union[int, list]) -> bool:
        if arg_id:
            add_to_id = set(self.recipient[__type])
            arg_id = {arg_id} if isinstance(arg_id, int) else set(arg_id)
            # 是否存在交集
            if arg_id & add_to_id:
                # 取出两者对称差集
                self.recipient[__type] = list(add_to_id ^ arg_id)
                await self._save()
                return True
        return False

    async def add_user(self, arg_id: int) -> bool:
        return await self._add("users", arg_id)

    async def remove_user(self, arg_id: int) -> bool:
        return await self._remove("users", arg_id)

    async def add_group(self, arg_id: int) -> bool:
        return await self._add("groups", arg_id)

    async def remove_group(self, arg_id: int) -> bool:
        return await self._remove("groups", arg_id)


__all__ = [
    "get_driver",
    "require",
    "config",
    "AnimeNews",
    "Recipient"
]
