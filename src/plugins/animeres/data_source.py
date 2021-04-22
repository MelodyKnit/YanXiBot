import aiohttp
from bs4 import BeautifulSoup
from typing import Iterator, Union


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
