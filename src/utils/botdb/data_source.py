import pymysql
from json import loads
from os.path import exists
from nonebot.log import logger
from pymysql.err import IntegrityError


CONFIG_DIR = "__config__\\" if exists("__config__") else "config\\"
INFO_TABLE_NAME = "user_info"


def read_config_file(path: str) -> dict:
    """
    :param path: MySQL 配置文件所在目录
    :return: MySQL配置参数
    """
    try:
        with open(path, mode="r") as file:
            return loads(file.read())
    except FileNotFoundError:
        return {}


def config(path: str, kwargs: dict) -> dict:
    """
    :param path: MySQL 配置文件所在目录
    :param kwargs: 可改改或者直接传入 MySQL配置参数
    :return: MySQL配置参数
    """
    return read_config_file(path or f"{CONFIG_DIR}mysql.json") | kwargs


class MySQLdb:
    INFO_TABLE_NAME = INFO_TABLE_NAME

    def __init__(self, *, path: str = None, **kwargs):
        self.connect = pymysql.connect(**config(path, kwargs))
        self.cursor = self.connect.cursor()

    def execute(self, query: str, args=None):
        self.cursor.execute(query, args)

    def execute_commit(self, query: str, args=None):
        try:
            self.cursor.execute(query, args)
            self.connect.commit()
        except IntegrityError:
            self.connect.rollback()

    def __del__(self):
        print("end===============")
        self.connect.close()
        self.cursor.close()


class DBMethods(MySQLdb):
    """
    集成在数据库的一些方法
    """
    __slots__ = ()

    def create_user_info_table(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self.INFO_TABLE_NAME}("
               "qid BIGINT PRIMARY KEY COMMENT '用户QQid',"
               "first_group BIGINT NOT NULL COMMENT '第一次注册所在群',"
               "nickname VARCHAR(16) COMMENT '用户名称',"
               "integral BIGINT NOT NULL DEFAULT 0 COMMENT '用户积分',"
               "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间'"
               ")")
        try:
            self.execute(sql)
            logger.info(f"{self.INFO_TABLE_NAME} 表初始化创建成功")
        except Warning:
            logger.warning(f"{self.INFO_TABLE_NAME} 表已存在，无需创建")

    def insert(self, query: str, args=None):
        self.execute_commit(f"insert into {query}", args)

    def update(self, query: str, args=None):
        self.execute_commit(f"update {query}", args)

    def select(self, query: str, args=None):
        self.execute(f"select {query}", args)
        return self.cursor.fetchall()

    def delete(self, query: str, args=None):
        self.execute_commit(f"delete from {query}", args)