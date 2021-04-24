import pymysql
from json import loads
from os.path import exists
from pymysql.err import IntegrityError


CONFIG_DIR = "__config__\\" if exists("__config__") else "config\\"
INFO_TABLE_NAME = "user_info"


def read_config_file(path: str) -> dict:
    try:
        with open(path, mode="r") as file:
            return loads(file.read())
    except FileNotFoundError:
        return {}


def config(path: str, kwargs: dict) -> dict:
    return read_config_file(path or f"{CONFIG_DIR}mysql.json") | kwargs


class MySQLdb:
    INFO_TABLE_NAME = INFO_TABLE_NAME

    def __init__(self, *, path: str = None, **kwargs):
        self.database = pymysql.connect(**config(path, kwargs))
        self.cursor = self.database.cursor()

    def execute(self, query, args=None):
        self.cursor.execute(query, args)

    def __del__(self):
        self.database.close()
        self.cursor.close()


class DBMethods(MySQLdb):
    """
    集成在数据库的一些方法
    """
    def create_user_info_table(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self.INFO_TABLE_NAME}("
               "qid BIGINT PRIMARY KEY COMMENT '用户QQid',"
               "first_group BIGINT NOT NULL COMMENT '第一次注册所在群',"
               "nickname VARCHAR(16) COMMENT '用户名称',"
               "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间'"
               ")")
        self.execute(sql)

    def insert(self, query: str, args=None):
        try:
            self.execute(f"insert into {query}", args)
            self.database.commit()
        except IntegrityError:
            self.database.rollback()

    def select(self, query: str, args=None):
        self.execute(f"select {query}", args)
        return self.cursor.fetchall()
