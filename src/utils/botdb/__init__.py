from nonebot.log import logger
from .data_source import DBMethods


class BotMethods:
    """
    机器人操作数据库的方法
    """
    conn: DBMethods = None

    def add_user(self, qid: int, gid: int):
        self.conn.insert(f"{self.conn.INFO_TABLE_NAME} "
                         f"(qid,first_group) values "
                         f"(%s,%s)", [qid, gid])

    def add_integral(self, qid: int, num: int):
        self.conn.update("user_info set integral=integral+%s where qid=%s", [num, qid])


class BotDB(BotMethods):
    __slots__ = ()

    def __init__(self):
        if not self.conn:
            logger.warning("not running!!!")

    def init(self):
        self.conn.create_user_info_table()


def run(path: str = None, **kwargs):
    BotMethods.conn = DBMethods(path=path, **kwargs)


def get_bot_db() -> BotDB:
    if BotMethods.conn:
        return BotDB()
    logger.error("not running!!!")

