import pymysql
from warnings import filterwarnings
from nonebot import get_driver


filterwarnings("error", category=pymysql.Warning)


class MySQLdb:
    def __init__(self):
        config = get_driver().config.mysql
        self.connect = pymysql.connect(**config)
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()
        self.cursor.close()

    def __del__(self):
        self.close()
