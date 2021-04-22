from nonebot.plugin import on_command
from nonebot.rule import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import get_driver
from pprint import pprint

from .config import Config
from .data_source import AnimeResSearch, AnimeResFilter

global_config = get_driver().config
config = Config(**global_config.dict())


anime_res = on_command("资源")


@anime_res.handle()
async def anime_res_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    state["res"] = None
    text = event.get_plaintext()
    if text:
        state["res"] = AnimeResFilter(*(await AnimeResSearch.get(text)))
        await state["res"].type_msg(anime_res)
        await anime_res.send("请选择所需类型")
    else:
        await anime_res.send("请输入资源名称也可以添加关键字，注意名称与关键字空格分隔。\n例如：天气之子或天气之子 mkv")


@anime_res.got("msg")
async def anime_res_got(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = event.get_plaintext()
    if state["res"]:
        await state["res"].confirm_type_msg(anime_res, text)
    else:
        if text:
            state["res"] = AnimeResFilter(*(await AnimeResSearch.get(state["msg"])))
            await state["res"].type_msg(anime_res)
            await anime_res.reject("请选择所需类型")
        await anime_res.reject("请输入资源名称！")









