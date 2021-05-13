from nonebot import on_notice
from .data_source import Increase, Decrease,\
    Bot, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent

group_notice = on_notice()


async def reply(notice):
    msg = await notice.reply()
    await group_notice.finish(msg)


@group_notice.handle()
async def group_increase_handle(bot: Bot, event: GroupIncreaseNoticeEvent):
    await reply(Increase(bot, event))


@group_notice.handle()
async def group_decrease_handle(bot: Bot, event: GroupDecreaseNoticeEvent):
    await reply(Decrease(bot, event))



