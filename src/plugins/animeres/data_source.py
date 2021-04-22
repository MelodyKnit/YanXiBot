import aiohttp
from bs4 import BeautifulSoup
from typing import Iterator, Union, Generator


def param(name, **kwargs) -> dict:
    return {
               "keyword": name,
           } | kwargs


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


async def resp(url: str, **kwargs) -> Union[BeautifulSoup, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as res:
            if res.status == 200:
                text = await res.text()
                return BeautifulSoup(text, "html.parser")
            raise TypeError(f"状态码: {res.status}")


class AnimeResSearch:
    main_url: str = "https://www.36dm.club/"
    search_url: str = f"{main_url}search.php"

    @staticmethod
    def get_page(html: BeautifulSoup) -> int:
        """
        :param html: 整个页面
        :return: 页数
        """
        html = html.find("div", {"class": "pages"})
        if html:
            return int(html.contents[-2].text)
        return 1

    @staticmethod
    def get_data_list(html: BeautifulSoup) -> Union[Iterator, None]:
        """
        :param html: 动漫数据列表
        :return 返回番剧
        """
        html = html.find(id="data_list")
        if html and not html.find_all("tr", {"class", "text_center"}):
            return (get_key_info(tr) for tr in html.find_all("tr"))
        return None

    @classmethod
    async def get_magnet(cls, href: str) -> Union[str, int]:
        """
        :param href: 数据表 get_data_list 中的 href
        :return: bt磁力链接
        """
        html = await resp(cls.main_url + href)
        return html.find(id="magnet")["href"]

    @classmethod
    async def get(cls, name: str, **kwargs) -> tuple[Iterator, BeautifulSoup]:
        """
        :param name: 番剧名字
        :param kwargs:
        :return: 迭代器和主页面两个参数
        """
        html: Union[BeautifulSoup, int] = await resp(cls.search_url, params=param(name, **kwargs))
        return cls.get_data_list(html), html


class AnimeResFilter:
    __slots__ = ("data", "html", "types")

    def __init__(self, data: Generator, html: BeautifulSoup = None):
        """
        :param data: 获取的资源的生成器
        :param html: 整个页面
        """
        self.data = dict()
        self.html = html
        self.types = []
        if data:
            for value in data:
                if value["type"] in self.types:
                    self.data[value["type"]].append(value)
                else:
                    self.types.append(value["type"])
                    self.data[value["type"]] = [value]

    async def type_msg(self, bot) -> str:
        """
        :param bot: 用于发送获取的信息
        :return: 当信息获取到时返回字符串让机器人发送
        当获取到类型时表示有资源
        如果资源类型只有一条便发送这一条数据
        否则发送所有类型
        """
        if self.types:
            if len(self.types) == 1:
                await self.confirm_type_send(bot, self.data[self.types[0]][0])
            await bot.send("获取类型如下:\n" + "\n".join([f"{i}. {t}" for i, t in enumerate(self.types)]))
        else:
            await bot.finish("未发现资源，先确认是否存在或输入是否有误！请重新输入。")
        return "请选择所需类型名或数字索引"

    async def confirm_type_msg(self, bot, text: str):
        """
        :param bot: 用于发送获取的信息
        :param text: 关键字文本
        判断文本是否能转为数字
        如果依然是字符串
            便通过字符串判断是否是以上类型中的一个，如果是便发送数据
        是数字
            查看是否能类型中的索引，如果是便发送数据
        """
        try:
            text = int(text)
        except ValueError:
            ...
        if isinstance(text, str):
            for t in self.types:
                if t in text:
                    await self.confirm_type_send(bot, self.data[t][0])
                continue
        else:
            if 0 <= text < len(self.types):
                await self.confirm_type_send(bot, self.data[self.types[text]][0])
        await bot.finish("您输入类型有误，请重新进行资源搜索！")

    @staticmethod
    async def confirm_type_send(bot, data: dict):
        """
        :param bot: 用于发送信息
        :param data: 获取的资源中的数据
        """
        text = f"名称：{data['title'][:80]}...\n大小：{data['size']}"
        magnet = await AnimeResSearch.get_magnet(data["href"])
        await bot.send(text)
        await bot.finish(magnet)



