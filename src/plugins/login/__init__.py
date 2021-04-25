from nonebot.rule import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command
from ...src.plugins.botdb import get_bot_db


bot_db = get_bot_db()

login = on_command("签到")


@login.handle()
async def login_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    print(event.get_plaintext())
