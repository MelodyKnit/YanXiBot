from .config import *
from pprint import pprint
from datetime import datetime
from time import localtime, time
from YanXiBot.src.utils.botdb.config import *
from YanXiBot.src.utils.botdb import get_bot_db

bot_db = get_bot_db()
bot_db.init()


class SignInMethods:
    __slots__ = ("user_id", "group_id", "user_info")

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id
        self.user_info = get_user_info(user_id)
        pprint(self.user_info)

    def sign_in(self):
        ...


def is_now(date: datetime) -> int:
    return localtime(time()).tm_mday - date.day


def sign_in(qid: int, num: int, continuous: bool):
    cont = "continuous_sign_times"
    cont = f"{cont}={cont}+i" if continuous else f"{cont}=1"
    bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s,{cont} where qid=%s", [num, qid])


def get_user_info(qid: int) -> list:
    return bot_db.select(f"* from {INFO_TABLE_NAME} where qid=%s", [qid])


def add_user(qid: int, gid: int, integral: int = 0):
    bot_db.insert(f"{INFO_TABLE_NAME} (qid,first_group,integral) values (%s,%s,%s)", [qid, gid, integral])


def set_integral(qid: int, num: int):
    bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s where qid=%s", [num, qid])


def is_user(qid: int) -> bool:
    return any(bot_db.raw_select(f"qid from {INFO_TABLE_NAME} where qid=%s", [qid]))


def get_sign_time(qid: int) -> datetime:
    return next(next(bot_db.raw_select(f"sign_time from {INFO_TABLE_NAME} where qid=%s", qid).__iter__()).__iter__())

