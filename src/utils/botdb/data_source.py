import pymysql
from warnings import filterwarnings
from nonebot.plugin import require

filterwarnings("error", category=pymysql.Warning)
read_config = require("readfile").read_config


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

    def close(self):
        self.connect.close()
        self.cursor.close()

    def __del__(self):
        self.close()
