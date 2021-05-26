"""
@Author         : melodyknit
@Date           : 2021-05-25 20:51:00
@LastEditors    : melodyknit
@LastEditTime   : 2021-05-25 20:51:00
@Description    : yhdm anime update message
@GitHub         : https://github.com/melodyknit
"""

from nonebot import require, get_driver
from nonebot.adapters.cqhttp import Bot
from .data_source import AnimeNews
scheduler = require("nonebot_plugin_apscheduler").scheduler
read_config = require("readfile").read_config


driver = get_driver()


def reply_message(message):
    return message


async def news(bot: Bot, group_ids: list):
    anime_news = await AnimeNews()
    for group_id in group_ids:
        await bot.send_group_msg(group_id=group_id, message=reply_message(anime_news.update()))
        await bot.send_group_msg(group_id=group_id, message=reply_message(anime_news.ranking()))


@driver.on_bot_connect
async def _(bot: Bot):
    values = await read_config("anime_news.yml")
    if values["group_id"]:
        scheduler.add_job(news, 'cron', hour=values["hour"], id='anime_update', args=[bot, values["group_id"]])
