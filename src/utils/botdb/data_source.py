import pymysql
from json import loads
from os.path import exists
from pymysql.err import IntegrityError
from warnings import filterwarnings


filterwarnings("error", category=pymysql.Warning)
CONFIG_DIR = "__config__\\" if exists("__config__") else "config\\"

# CONFIG_DIR = "..\\..\\..\\__config__\\"


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
        self.connect.close()
        self.cursor.close()
