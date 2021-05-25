from aiomysql import connect, Warning, Connection, Cursor, \
    IntegrityError, InternalError, OperationalError, Error
from nonebot import get_driver, require
from warnings import filterwarnings
from nonebot.log import logger

from .config import Config

config = Config()
driver = get_driver()
read_config = require("readfile").read_config
filterwarnings("error", category=Warning)


class MySQLdbMethods:
    __slots__ = ("_conn", "cur", "description")
    cur: Cursor
    is_run = False                  # 数据库是否启动
    _conn: Connection
    config = driver.config.mysql    # mysql配置

    async def execute(self, query: str, param: list = None):
        await self.cur.execute(query, param)

    async def execute_commit(self, query: str, param: list = None):
        try:
            await self.cur.execute(query, param)
            await self._conn.commit()
        except IntegrityError:
            await self._conn.rollback()

    def fetchall(self):
        return self.cur.fetchall()

    @classmethod
    async def connect(cls):
        """
        与数据库建立连接
        """
        try:
            cls._conn = await connect(**cls.config)
            cls.cur = await cls._conn.cursor()
            logger.info("成功与MySQL数据库建立连接！")
        except OperationalError as err:
            logger.error("数据库连接失败！请检查配置文件是否输入有误！")
            assert False, err
        return True

    @classmethod
    async def init_table(cls):
        """
        进行初始化建立数据表
        """
        if driver.config.mysql_init:
            try:
                sql = await read_config(config.file_path)
                await cls.cur.execute(sql)
                logger.info("数据表初始化建立成功！")
            except Warning:
                logger.warning("数据表已建立，无需重复建立，请忽略该Warning，如需停止Warning请更改配置文件中的mysql_init=false")
            except InternalError as err:
                logger.error("数据表创建失败，请检查并更新数据库！")
                assert False, err
        return True

    @classmethod
    async def run(cls):
        """
        启动数据库
        """
        try:
            await cls.connect()
            await cls.init_table()
        except AssertionError as err:
            logger.error(err)
        else:
            cls.is_run = True

    @classmethod
    async def close(cls):
        """
        关闭数据库
        """
        await cls.cur.close()
        cls._conn.close()


driver.on_startup(MySQLdbMethods.run)
driver.on_shutdown(MySQLdbMethods.close)
