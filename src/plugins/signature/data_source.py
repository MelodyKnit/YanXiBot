from .config import *
from datetime import datetime
from YanXiBot.src.utils.botdb.config import *
from YanXiBot.src.utils.botdb import get_bot_db


bot_db = get_bot_db()
bot_db.init()


class SignInMethods:
    __slots__ = ("user_id", "group_id", "user_info", "merge")

    def __init__(self, user_id: int, group_id: int):
        self.merge = INTEGRAL_UNIT + INTEGRAL_NAME
        self.user_id = user_id
        self.group_id = group_id
        self.user_info = get_user_info(user_id)
        if not self.user_info:
            add_user(user_id, group_id)
            self.user_info = get_user_info(user_id)

    def sign_in(self) -> str:
        sign_time = self.user_info["sign_time"]
        number = ADD_INTEGRAL_NUMBER
        if sign_time:
            number = self.sign_in_full(sign_time)
            if not number:
                return "您今天已经签到过了哟！"
        else:
            sign_in(self.user_id, number, True)
        self.user_info["sign_number_times"] += 1
        self.user_info["continuous_sign_times"] += 1
        return (f"签到成功今日获得{number}{self.merge}\n"
                f"累计签到：{self.user_info['sign_number_times']}天\n"
                f"连续签到：{self.user_info['continuous_sign_times']}天")

    def sign_in_full(self, sign_day: datetime) -> int:
        """
        :param sign_day: 签到时间
        :return: 如果今天签到成功返回签到所得到的数量，如果没有返回none
        """
        days = (datetime.today() - sign_day).days
        if days:
            number, not_now = ADD_INTEGRAL_NUMBER, days == 1
            if not_now:
                number += self.user_info["continuous_sign_times"]
            else:
                self.user_info["continuous_sign_times"] = 0
            sign_in(self.user_id, number, not_now)
            return number


def sign_in(qid: int, num: int, continuous: bool):
    cont = "continuous_sign_times"
    cont = f"{cont}={cont}+1" if continuous else f"{cont}=1"
    bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s,"
                  f"sign_number_times=sign_number_times+1,{cont},"
                  f"sign_time=now() where qid=%s", [num, qid])


def get_user_info(qid: int) -> dict:
    user_info = bot_db.select_all(f"{INFO_TABLE_NAME} where qid=%s", [qid])
    if user_info:
        return user_info[0]


def add_user(qid: int, gid: int):
    bot_db.insert(f"{INFO_TABLE_NAME} (qid,first_group) values (%s,%s)", [qid, gid])


def get_sign_time(qid: int) -> datetime:
    return next(next(bot_db.select(f"sign_time from {INFO_TABLE_NAME} where qid=%s", qid).__iter__()).__iter__())
