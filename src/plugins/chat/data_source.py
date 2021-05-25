import aiohttp
from json import loads
from nonebot import require
from .config import Config
from random import choice


config = Config()
base_url = "http://i.itpk.cn/api.php"
read_data = require("readfile").read_data


def get_params(msg: str):
    return {
        "question": msg,
        "limit": 8,
        "api_key": "1447d08d8e018247e2ce829e9d0380e8",
        "api_secret": "p782g4wij4b0"
    }


async def get_message_reply(msg: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, params=get_params(msg)) as resp:
            try:
                text = loads((await resp.text()).encode("utf-8"))
                try:
                    return text["content"]
                except KeyError:
                    return "抱歉，为对数据进行整理目前无法使用"
            except ValueError:
                return await resp.text()


async def data_in_msg(msg: str):
    data = await read_data(config.data_path)
    for i in data:
        if i in msg:
            return choice(data[i])


class ChatMessageReply:
    __slots__ = ("msg",)
    _reply = [
        data_in_msg,
        get_message_reply
    ]

    def __init__(self, msg: str):
        self.msg = msg

    async def reply(self):
        for i in self._reply:
            msg = await i(self.msg)
            if msg:
                return msg
