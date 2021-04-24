import pymysql
from json import loads
from pymysql.err import IntegrityError

INFO_TABLE_NAME = "user_info"


def read_config_file(path: str) -> dict:
    try:
        with open(path, mode="r") as file:
            return loads(file.read())
    except FileNotFoundError:
        return {}


def config(path: str, kwargs: dict) -> dict:
    return read_config_file(path or "mysql.json") | kwargs


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
