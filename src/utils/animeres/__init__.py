from bs4 import BeautifulSoup
from typing import Generator
from .data_source import AnimeResSearch

get = AnimeResSearch.get


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










