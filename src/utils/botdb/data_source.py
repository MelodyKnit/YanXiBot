import pymysql
from pymysql.err import IntegrityError
from warnings import filterwarnings
from YanXiBot.src.utils.readfile import read_config

filterwarnings("error", category=pymysql.Warning)


def config(path: str, kwargs: dict) -> dict:
    """
    :param path: MySQL 配置文件所在目录
    :param kwargs: 可改改或者直接传入 MySQL配置参数
    :return: MySQL配置参数
    """
    return read_config(path) or {} | kwargs


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
