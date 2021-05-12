from .config import Config
from nonebot.log import logger
from .data_source import MySQLdb
from nonebot.plugin import export
from pymysql.err import IntegrityError

export = export()
config = Config()


class DBMethods:
    """
    机器人操作数据库的方法
    """
    INFO_TABLE = config.info_table_name
    db: MySQLdb = None

    def execute(self, query: str, args=None):
        self.db.cursor.execute(query, args)

    def execute_commit(self, query: str, args=None):
        try:
            self.db.cursor.execute(query, args)
            self.db.connect.commit()
        except IntegrityError:
            self.db.connect.rollback()

    def insert(self, query: str, args=None):
        self.execute_commit(f"insert into {query}", args)

    def update(self, query: str, args=None):
        self.execute_commit(f"update {query}", args)

    def select_all(self, query: str, args=None) -> list:
        self.execute(f"select * from {query}", args)
        return [{next(title.__iter__()): data
                for title, data in zip(self.db.cursor.description, table)}
                for table in self.db.cursor.fetchall()]

    def select(self, query: str, args=None) -> tuple:
        self.execute(f"select {query}", args)
        return self.db.cursor.fetchall()

    def delete(self, query: str, args=None):
        self.execute_commit(f"delete from {query}", args)


class BotInitTable(DBMethods):
    def create_user_info_table(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self.INFO_TABLE}("
               "qid BIGINT PRIMARY KEY COMMENT '用户QQid',"
               "nickname VARCHAR(16) COMMENT '用户名称',"
               "integral BIGINT NOT NULL DEFAULT 0 COMMENT '用户积分',"
               "sign_time TIMESTAMP COMMENT '签到时间',"
               "first_group BIGINT NOT NULL COMMENT '第一次注册所在群',"
               "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',"
               "sign_number_times SMALLINT NOT NULL  DEFAULT 0 COMMENT '累计签到次数',"
               "continuous_sign_times SMALLINT NOT NULL DEFAULT 0 COMMENT '连续签到次数'"
               ")")
        try:
            self.execute(sql)
            logger.info(f"{self.INFO_TABLE} 表初始化创建成功")
        except Warning:
            logger.warning(f"{self.INFO_TABLE} 表已存在，无需创建")


class BotDB(BotInitTable):
    __slots__ = ()

    def __init__(self, is_init):
        if is_init:
            self.init()

    def init(self):
        self.create_user_info_table()


def run():
    if not DBMethods.db:
        DBMethods.db = MySQLdb()
    else:
        logger.warning("请勿重复启动数据库！")


def get_bot_db(is_init: bool = False) -> BotDB:
    """
    :param is_init: bool 是否对数据库进行初始化
    """
    if DBMethods.db:
        return BotDB(is_init)
    logger.error("数据库未运行！！！")


export.run = run
export.get_bot_db = get_bot_db

