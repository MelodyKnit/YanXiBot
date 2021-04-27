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

    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id
        self.user_info = get_user_info(user_id)
        if not self.user_info:
            add_user(user_id, group_id)
            self.user_info = get_user_info(user_id)
        self.user_info = self.user_info[0]

    def sign_in(self):
        day_time = self.user_info["sign_time"]
        print(day_time)


def is_now(date: datetime) -> int:
    return localtime(time()).tm_mday - date.day


def sign_in(qid: int, num: int, continuous: bool):
    cont = "continuous_sign_times"
    cont = f"{cont}={cont}+i" if continuous else f"{cont}=1"
    bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s,{cont} where qid=%s", [num, qid])


def get_user_info(qid: int) -> list:
    return bot_db.select(f"* from {INFO_TABLE_NAME} where qid=%s", [qid])


def add_user(qid: int, gid: int):
    bot_db.insert(f"{INFO_TABLE_NAME} (qid,first_group) values (%s,%s)", [qid, gid])


def set_integral(qid: int, num: int):
    bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s where qid=%s", [num, qid])


def is_user(qid: int) -> bool:
    return any(bot_db.raw_select(f"qid from {INFO_TABLE_NAME} where qid=%s", [qid]))


def get_sign_time(qid: int) -> datetime:
    return next(next(bot_db.raw_select(f"sign_time from {INFO_TABLE_NAME} where qid=%s", qid).__iter__()).__iter__())

