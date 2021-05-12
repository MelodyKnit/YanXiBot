from nonebot.rule import T_State
from nonebot import on_command, require
from nonebot.adapters.cqhttp import Bot, MessageEvent
from .data_source import get_anime_res, ReplyMessage


separate_trigger = require("rules").separate_trigger
anime_res = on_command("资源", rule=separate_trigger, aliases={"动漫资源"})


@anime_res.handle()
async def anime_res_handle(bot: Bot, event: MessageEvent, state: T_State):
    state["res"] = None
    text = event.get_plaintext()
    if text:
        state["res"], msg = await get_anime_res(anime_res, text)
        await anime_res.send(msg)
    else:
        await anime_res.send("请输入资源名称也可以添加关键字，注意名称与关键字空格分隔。\n例如：天气之子或天气之子 mkv")


@anime_res.got("msg")
async def anime_res_got(bot: Bot, event: MessageEvent, state: T_State):
    text = event.get_plaintext()
    if state["res"]:
        await state["res"].reply_magnet(text)
    else:
        if text:
            state["res"], msg = await get_anime_res(anime_res, text)
            await anime_res.reject(msg)
        await anime_res.reject("请输入资源名称！")
