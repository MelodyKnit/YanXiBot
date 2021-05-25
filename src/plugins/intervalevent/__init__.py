from nonebot.adapters.cqhttp import Bot
from nonebot import get_driver
from nonebot import require
from typing import Union

from .config import Config


driver = get_driver()
bot_me: Union[Bot, None] = None
global_config = get_driver().config
config = Config(**global_config.dict())
scheduler = require("nonebot_plugin_apscheduler").scheduler


# @driver.on_bot_connect
# async def _(bot: Bot):
#     global bot_me
#     bot_me = bot
#
#
# @driver.on_bot_disconnect
# async def _(bot: Bot):
#     global bot_me
#     bot_me = None
#
#
# @scheduler.scheduled_job('cron', second='*')
# async def _():
#     if bot_me:
#         ...
