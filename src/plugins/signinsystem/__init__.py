from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.rule import T_State
from nonebot import get_driver, on_command, require
from pprint import pprint
from .data_source import SignIn
from .config import Config

BotDBMethods = require("botdb").BotDBMethods
global_config = get_driver().config
config = Config(**global_config.dict())

login_in = on_command("签到")
db = BotDBMethods()


@login_in.handle()
async def login_in_handle(bot: Bot, event: GroupMessageEvent):
    async with SignIn(event.user_id, event.group_id) as sign:
        await login_in.finish(await sign.sign_in())


