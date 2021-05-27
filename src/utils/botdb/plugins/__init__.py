"""
说明:
    用于连接上某个数据库时的启动事件，后期可能会编写多个数据库，当某个数据无法连接等切换到其他数据库
"""
from .mysqldb import MySQLdbMethods

bot_db_run_event = []
bot_db_stop_event = []


def on_bot_db_run(func):
    """注册一个在数据库连接成功后运行的函数"""
    bot_db_run_event.append(func)


def on_bot_db_stop(func):
    """注册一个在数据库连接停止后运行的函数"""
    bot_db_stop_event.append(func)


@MySQLdbMethods.on_bot_db_run
async def _():
    [await event() for event in bot_db_run_event]


@MySQLdbMethods.on_bot_db_stop
async def _():
    [await event() for event in bot_db_stop_event]


__all__ = [
    "on_bot_db_run",
    "on_bot_db_stop"
]
