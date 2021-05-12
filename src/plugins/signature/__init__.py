from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command, on_regex
from .data_source import SignIn

sign_in = on_regex(r"^[签到]$")
sign_query = on_regex(r"^查询$")


@sign_in.handle()
async def sign_in_handle(bot: Bot, event: GroupMessageEvent):
    method = SignIn(event.user_id, event.group_id)
    msg = method.sign_in()
    await sign_in.finish(msg)


@sign_query.handle()
async def sign_query_handle(bot: Bot, event: GroupMessageEvent):
    method = SignIn(event.user_id, event.group_id)
    msg = method.query_info()
    await sign_in.finish(msg)



