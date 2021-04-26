from nonebot.rule import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command
from .data_source import SignInMethods

login = on_command("签到")


@login.handle()
async def login_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    info = SignInMethods(event.user_id, event.group_id)
    # print(info.sign_in())
    # if is_user(event.user_id):
    #     ...
