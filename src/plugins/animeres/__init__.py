from nonebot.rule import T_State
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, Event
from .data_source import get_anime_res, ReplyMessage


async def _is_group(bot: Bot, event: Event, state: T_State):
    event: GroupMessageEvent
    if "group_id" not in state:
        state["group_id"] = event.group_id
    return state["group_id"] == event.group_id


anime_res = on_command("资源", rule=_is_group, aliases={"动漫资源"})


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
    text = event.get_plaintext()
    if state["res"]:
        await state["res"].reply_magnet(text)
    else:
        if text:
            state["res"], msg = await get_anime_res(anime_res, text)
            await anime_res.reject(msg)
        await anime_res.reject("请输入资源名称！")
