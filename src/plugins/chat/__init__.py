from nonebot.rule import to_me
from nonebot import get_driver, on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent
from .config import Config

# ------------------------------

from .data_source import get_message_reply

# ------------------------------

global_config = get_driver().config
config = Config(**global_config.dict())

# ------------------------------

chat = on_message(rule=to_me())


@chat.handle()
async def chat_handle(bot: Bot, event: MessageEvent):
    if str(event.message):
        msg = await get_message_reply(str(event.message))
        await chat.finish(msg)
    await chat.finish("亲爱的怎么啦！有什么事吗？")
