from nonebot.rule import T_State
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import get_anime_res, ReplyMessage


anime_res = on_command("资源", aliases={"动漫资源"})


async def this_group(event, state):
    if state["group_id"] != event.group_id:
        await anime_res.reject()


@anime_res.handle()
async def anime_res_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    state["group_id"] = event.group_id
    state["res"] = None
    text = event.get_plaintext()
    if text:
        state["res"], msg = await get_anime_res(anime_res, text)
        await anime_res.send(msg)
    else:
        await anime_res.send("请输入资源名称也可以添加关键字，注意名称与关键字空格分隔。\n例如：天气之子或天气之子 mkv")


@anime_res.got("msg")
async def anime_res_got(bot: Bot, event: GroupMessageEvent, state: T_State):
    await this_group(event, state)
    text = event.get_plaintext()
    if state["res"]:
        await state["res"].reply_magnet(text)
    else:
        if text:
            state["res"], msg = await get_anime_res(anime_res, text)
            await anime_res.reject(msg)
        await anime_res.reject("请输入资源名称！")
