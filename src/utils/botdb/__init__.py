from config import *
from nonebot.log import logger
from data_source import MySQLdb


class DBMethods:
    """
    机器人操作数据库的方法
    """
    INFO_TABLE_NAME = INFO_TABLE_NAME
    db: MySQLdb = None

    def create_user_info_table(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self.INFO_TABLE_NAME}("
               "nickname VARCHAR(16) COMMENT '用户名称',"
               "qid BIGINT PRIMARY KEY COMMENT '用户QQid',"
               "first_group BIGINT NOT NULL COMMENT '第一次注册所在群',"
               "integral BIGINT NOT NULL DEFAULT 0 COMMENT '用户积分',"
               "sign_number_times SMALLINT NOT NULL  DEFAULT 0 COMMENT '累计签到次数',"
               "continuous_sign_times SMALLINT NOT NULL DEFAULT 0 COMMENT '连续签到次数',"
               "sign_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '签到时间',"
               "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间'"
               ")")
        try:
            self.db.execute(sql)
            logger.info(f"{self.INFO_TABLE_NAME} 表初始化创建成功")
        except Warning:
            logger.warning(f"{self.INFO_TABLE_NAME} 表已存在，无需创建")

    def insert(self, query: str, args=None):
        self.db.execute_commit(f"insert into {query}", args)

    def update(self, query: str, args=None):
        self.db.execute_commit(f"update {query}", args)

    def select(self, query: str, args=None):
        self.db.execute(f"select {query}", args)
        return self.db.cursor.fetchall()

    def delete(self, query: str, args=None):
        self.db.execute_commit(f"delete from {query}", args)


class BotDB(DBMethods):
    __slots__ = ()

    def __init__(self, is_init):
        self.execute = lambda query, args=None: self.db.execute(query, args)
        self.execute_commit = lambda query, args=None: self.db.execute_commit(query, args)
        if is_init:
            self.init()

    def init(self):
        self.create_user_info_table()


def run(path: str = None, **kwargs):
    DBMethods.db = MySQLdb(path=path, **kwargs)


def get_bot_db(is_init: bool = False) -> BotDB:
    if DBMethods.db:
        return BotDB(is_init)
    logger.error("数据库未运行！！！")