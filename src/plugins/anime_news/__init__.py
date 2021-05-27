"""
@Author         : melodyknit
@Date           : 2021-05-25 20:51:00
@LastEditors    : melodyknit
@LastEditTime   : 2021-05-27 15:51:00
@Description    : yhdm anime update message
@GitHub         : https://github.com/melodyknit
"""

from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, Message
from nonebot import on_command
from nonebot.permission import SUPERUSER
from asyncio import sleep
from typing import Optional
from .data_source import AnimeNews, Recipient, config, require, get_driver
from .methods import GetAllId

scheduler = require("nonebot_plugin_apscheduler").scheduler
recipient: Optional[Recipient] = None
SendInfo = config.SendInfo
driver = get_driver()

addRecipient = on_command("添加推送", permission=SUPERUSER, priority=1, block=True)
removeRecipient = on_command("移除推送", permission=SUPERUSER, priority=1, block=True)


@addRecipient.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    all_id = GetAllId(Message(event.raw_message))
    if all_id.all_none():
        all_id.group_id.append(event.group_id)
    if await recipient.add_user(all_id.user_id) or await recipient.add_group(all_id.group_id):
        await addRecipient.finish("每日新番消息推送添加成功")
    await addRecipient.finish("已经添加过了哟！")


@removeRecipient.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    all_id = GetAllId(Message(event.raw_message))
    if all_id.all_none():
        all_id.group_id.append(event.group_id)
    if await recipient.remove_user(all_id.user_id) or await recipient.remove_group(all_id.group_id):
        await addRecipient.finish("已经从每日新番消息推送中移除")
    await addRecipient.finish("该群已不在推送范围！")


async def send(bot: Bot, info: SendInfo):
    for send_id in info.send_list:
        if send_id in info.id_list:
            for news in info.news_list:
                await bot.call_api(info.api, self_id=bot.self_id, **{
                    info.id_type: send_id
                }, message=news)
                await sleep(driver.config.dict().get("send_news_sleep") or 0)
        else:
            await info.remove(send_id)


async def send_private(bot: Bot, news_list: list):
    """ 发送给所有需要发送的用户"""
    await send(bot, SendInfo({
        "api": "send_private_msg",
        "id_type": "user_id",
        "id_list": [i["user_id"]for i in await bot.get_friend_list()],
        "send_list": recipient.users,
        "news_list": news_list,
        "remove": recipient.remove_user
    }))


async def send_group(bot: Bot, news_list: list):
    """ 发送给所有需要发送的群"""
    await send(bot, SendInfo({
        "api": "send_group_msg",
        "id_type": "group_id",
        "id_list": [i["group_id"] for i in await bot.get_group_list()],
        "send_list": recipient.groups,
        "news_list": news_list,
        "remove": recipient.remove_group
    }))


async def send_news(bot: Bot):
    anime_news: AnimeNews = await AnimeNews()
    news_list = [anime_news.update(), anime_news.ranking()]
    await send_private(bot, news_list)
    await send_group(bot,  news_list)


@driver.on_bot_connect
async def _(bot: Bot):
    global recipient
    recipient = await Recipient()
    if driver.config.dict().get("send_news_time") is not None:
        scheduler.add_job(send_news, 'cron',
                          hour=driver.config.send_news_time,
                          id='anime_news', args=[bot])
