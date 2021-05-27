from nonebot.rule import to_me
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent
from .data_source import get_message_reply, ChatMessageReply
chat = on_message(rule=to_me(), priority=10)


@chat.handle()
async def chat_handle(bot: Bot, event: MessageEvent):
    if str(event.message):
        reply = ChatMessageReply(event.get_plaintext())
        msg = await reply.reply()
        await chat.finish(msg)
    await chat.finish("亲爱的怎么啦！有什么事吗？")
