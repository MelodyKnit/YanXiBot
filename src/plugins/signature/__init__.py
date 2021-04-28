from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command
from .data_source import SignInMethods

login = on_command("签到")


@login.handle()
async def login_handle(bot: Bot, event: GroupMessageEvent):
    info = SignInMethods(event.user_id, event.group_id)
    await login.finish(info.sign_in())
