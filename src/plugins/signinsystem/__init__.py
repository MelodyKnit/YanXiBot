from nonebot.adapters.cqhttp import Bot, MessageEvent, Event
from nonebot import get_driver, on_command
from .data_source import SignIn
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

login_in = on_command("签到")
login_in_query = on_command("查询", aliases={"状态"})


@login_in.handle()
async def login_in_handle(bot: Bot, event: MessageEvent):
    async with SignIn(event.user_id, event.dict().get("group_id")) as sign:
        await login_in.finish(sign.sign_in())


@login_in_query.handle()
async def login_in_query_handle(bot: Bot, event: MessageEvent):
    async with SignIn(event.user_id) as sign:
        await login_in_query.finish(sign.query())


