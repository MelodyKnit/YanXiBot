#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot
from YanXiBot.src.utils import botdb


botdb.run()
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot)

nonebot.load_builtin_plugins()
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("src/plugins")
# nonebot.load_plugins("src/utils")


# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
