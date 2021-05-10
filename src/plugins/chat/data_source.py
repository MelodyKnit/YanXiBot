import aiohttp
from json import loads

base_url = "http://i.itpk.cn/api.php"


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

