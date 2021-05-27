from pathlib import Path

from nonebot import get_driver, load_plugins, require, logger

from .config import Config

on_bot_db_run = require("botdb").on_bot_db_run

global_config = get_driver().config
config = Config(**global_config.dict())


@on_bot_db_run
async def _():
    logger.info("加载与数据库相关插件")
    _sub_plugins = set()
    _sub_plugins |= load_plugins(
        str((Path(__file__).parent / "plugins").resolve()))
