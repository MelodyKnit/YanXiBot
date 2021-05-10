from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command
from .data_source import SignIn

sign_in = on_command("签到")
sign_query = on_command("查询", aliases={"属性"})


@sign_in.handle()
async def sign_in_handle(bot: Bot, event: GroupMessageEvent):
    method = SignIn(event.user_id, event.group_id)
    msg = method.sign_in()
    await sign_in.finish(msg)


@sign_query.handle()
async def sign_query_handle(bot: Bot, event: GroupMessageEvent):
    js = bot.config.json()
    print(js)
    print(dir(bot.config))
    method = SignIn(event.user_id, event.group_id)
    msg = method.query_info()
    await sign_in.finish(msg)



