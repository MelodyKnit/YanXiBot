import aiohttp
from nonebot.matcher import Matcher
from bs4 import BeautifulSoup
from typing import Union, Type
headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 ('
                         'KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}


def param(name) -> dict:
    return {"keyword": name}


def get_key_info(tr: BeautifulSoup) -> dict:
    td = tr.find_all("td")
    title = td[2].find("a")
    return {
        "time": td[0].text,
        "type": td[1].text,
        "title": title.text.strip().replace("\n", " "),
        "href": title["href"],
        "keyword": [key.text for key in title.find_all("span", {"class": "keyword"})],
        "size": td[3].text,
        "author": td[7].text
    }


async def resp(url: str, **kwargs) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, **kwargs) as res:
            if res.status == 200:
                text = await res.text()
                return BeautifulSoup(text, "html.parser")


class AnimeRes:
    main_url = "https://www.36dm.club/"
    search_url = f"{main_url}search.php"
    __slots__ = ("html", "name")

    def __init__(self, html: BeautifulSoup, name: str):
        self.html, self.name = html, name

    def get_page(self) -> int:
        """
        获取页面页数
        :return: 页数
        """
        html = self.html.find("div", {"class": "pages"})
        return int(html.contents[-2].text) if html else 1

    def get_data_dict(self) -> Union[dict, None]:
        """
        返回数据为 none 表示无数据
        :return dict 返回番剧
        """
        html = self.html.find(id="data_list")
        data = {}
        if html and not html.find_all("tr", {"class", "text_center"}):
            for tr in html.find_all("tr"):
                value = get_key_info(tr)
                if value["type"] in data.keys():
                    data[value["type"]].append(value)
                else:
                    data[value["type"]] = [value]
        return data

    @classmethod
    async def get_magnet(cls, href: str) -> str:
        """
        获取资源的 magnet
        :param href: 数据表 get_data_list 中的 href
        :return: bt磁力链接
        """
        html = await resp(cls.main_url + href)
        return html.find(id="magnet")["href"]


class ReplyMessage:
    __slots__ = ("res", "matcher", "data", "keys")
    number_of_errors = 0

    def __init__(self, matcher: Type[Matcher], res: AnimeRes):
        self.res = res
        self.matcher = matcher
        self.data = res.get_data_dict()
        self.keys = list(self.data.keys())

    async def reply(self) -> str:
        """
        如果未发现资源会在终止
        :return: 获取到的类型
        """
        if not self.keys:
            await self.matcher.finish("抱歉主人，未发现该动漫的资源，请确认一下是否输入有误呢！")
        return "请选择您想要的类型：\n" + "\n".join([f"{i + 1}.{v}" for i, v in enumerate(self.keys)])

    async def send_magnet(self, data: dict):
        data = data[0]
        magnet = await self.res.get_magnet(data["href"])
        await self.matcher.send(f"名称：{data['title'][:90]}...\n"
                                f"大小：{data['size']}")
        await self.matcher.finish(magnet)

    async def reply_magnet(self, key: str):
        """
        传入类型判断该类型是否存在并进行回复
        :param key: 类型
        """
        if key.isdigit():
            key = int(key) - 1
            if 0 <= key < len(self.keys):
                await self.send_magnet(self.data[self.keys[key]])
        else:
            for k in self.keys:
                if k in key:
                    await self.send_magnet(self.data[k])
        await self.matcher.finish("输入类型有误，请重新获取资源！")


async def get_anime_res(matcher: Type[Matcher], name: str):
    """
    :param matcher:
    :param name: 片名
    :return: 返回资源实列
    """
    try:
        html = await resp(AnimeRes.search_url, params=param(name))
        res = ReplyMessage(matcher, AnimeRes(html, name))
        return res, await res.reply()
    except TypeError as err:
        await matcher.finish(f"请求错误，异常内容如下：\n{err}")
