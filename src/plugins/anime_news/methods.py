from re import compile
from nonebot.adapters.cqhttp import Message


class GetAllId:
    _re_id = compile(r"\d+")

    def __init__(self, message: Message):
        self.group_id = []
        self.user_id = []
        for msg in message:
            if msg.type == "text":
                self.group_id += list(map(int, self._re_id.findall(msg.data.get("text"))))
            elif msg.type == "at":
                self.user_id.append(int(msg.data.get("qq")))

    def all_none(self):
        return not(self.user_id or self.group_id)


__all__ = [
    "GetAllId"
]
