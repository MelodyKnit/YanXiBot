from nonebot import export
from .plugins.mysqldb import SQLMethods
from .plugins import on_bot_db_run, on_bot_db_stop


class BotDBMethods:
    """
    作为机器人数据库操作规范
    在plugin构建数据库或者文件数据库
    cursor方法回去获取
    """
    __slots__ = ()

    @property
    def cursor(self) -> SQLMethods:
        if SQLMethods.is_run:
            return SQLMethods()

    async def insert(self, __table: str, **kwargs):
        await self.cursor.insert(__table, **kwargs)

    async def update(self, __table: str, **kwargs):
        await self.cursor.update(__table, **kwargs)

    async def delete(self, __table: str, *args, **kwargs):
        await self.cursor.delete(__table, *args, **kwargs)

    async def select(self, __table: str, *args, **kwargs) -> list:
        return await self.cursor.select(__table, *args, **kwargs)


export = export()
export.BotDBMethods = BotDBMethods
export.on_bot_db_run = on_bot_db_run
export.on_bot_db_stop = on_bot_db_stop
