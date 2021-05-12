from nonebot import export
from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent
from nonebot.rule import T_State
from .config import Config


global_config = get_driver().config
config = Config(**global_config.dict())
export = export()


async def separate_trigger(bot: Bot, event: Event, state: T_State):
    """
    群里事件与私人事件分离
    并且群与群之间分离
    """
    if "event" not in state:
        state["event"] = event
    else:
        if state["event"] is not event:
            return False
    if isinstance(event, GroupMessageEvent):
        event: GroupMessageEvent
        if "group_id" not in state:
            state["group_id"] = event.group_id
        return state["group_id"] == event.group_id
    return True

export.separate_trigger = separate_trigger


