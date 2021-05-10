<h1 align="center">Anime Res Search</h1>

```python
from nonebot.plugin import on_command
from nonebot.rule import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent

from .data_source import AnimeResFilter, get

anime_res = on_command("资源", aliases={"动漫资源"})


@anime_res.handle()
async def anime_res_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    state["res"] = None
    text = event.get_plaintext()
    if text:
        state["res"] = AnimeResFilter(*(await get(text)))
        msg = await state["res"].type_msg(anime_res)
        await anime_res.send(msg)
    else:
        await anime_res.send("请输入资源名称也可以添加关键字，注意名称与关键字空格分隔。\n例如：天气之子或天气之子 mkv")


@anime_res.got("msg")
async def anime_res_got(bot: Bot, event: GroupMessageEvent, state: T_State):
    text = event.get_plaintext()
    if state["res"]:
        await state["res"].confirm_type_msg(anime_res, text)
    else:
        if text:
            state["res"] = AnimeResFilter(*(await get(state["msg"])))
            msg = await state["res"].type_msg(anime_res)
            await anime_res.reject(msg)
        await anime_res.reject("请输入资源名称！")
```
