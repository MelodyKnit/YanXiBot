from typing import Union
from random import choice
from .config import Config
from nonebot import require
from datetime import datetime
from nonebot.adapters.cqhttp import Bot, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent,\
    Message, MessageSegment

config = Config()
read_config = require("readfile").read_config
GroupNoticeEvent = Union[GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent]


class ReplyMessage:
    typeof: str

    def __init__(self, bot: Bot, event: GroupNoticeEvent):
        self.bot = bot
        self.event = event
        self.config = {}

    async def set_config(self):
        self.config = await read_config(config.file_path)

    # 需要格式化字符
    async def format_keys(self, more: dict = None) -> dict:
        more = more or {}
        return {
            "uid": self.event.user_id,
            "gid": self.event.group_id,
            "oid": self.event.operator_id,
            "time": datetime.fromtimestamp(self.event.time),
            **more
        }

    # 消息回复
    async def reply(self) -> Message:
        await self.set_config()
        msg = self.config[self.typeof]["merge"] or self.config[self.typeof]
        msg: str = choice(msg) if self.config["Random"][self.typeof] else msg[0]
        return Message(msg.format(**(await self.format_keys())))


class Increase(ReplyMessage):
    event: GroupIncreaseNoticeEvent
    typeof = "IncreaseMessage"

    async def format_keys(self, more: dict = None) -> dict:
        """
        获取新加入用户的信息进行回复
        """
        more = more or {}
        user_info = await self.bot.get_group_member_info(group_id=self.event.group_id, user_id=self.event.user_id)
        return await super(Increase, self).format_keys({
            "name": user_info["nickname"],
            "sex": user_info["sex"],
            "at": MessageSegment.at(user_info["user_id"]),
            **more})


class Decrease(ReplyMessage):
    event: GroupDecreaseNoticeEvent
    typeof = "DecreaseMessage"
