from nonebot.rule import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command

# bot_db.init()

login = on_command("签到")


@login.handle()
async def login_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    ...
    # if not bot_db.select_user(event.user_id):
    #     bot_db.add_user(event.user_id, event.group_id)
    #     await login.finish("签到成功")
    # else:
    #     await login.finish("已经签到过了")
