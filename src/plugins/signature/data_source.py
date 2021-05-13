from nonebot.plugin import require
from datetime import datetime
from typing import Union
from .config import *

bot_db = require("botdb")

bot_db.run()
INFO_TABLE_NAME: str = bot_db.info_table
bot_db = bot_db.get_bot_db(True)


class Methods:
    __slots__ = ("user_id", "group_id", "user_info", "merge")

    def add_integral(self, num: int, continuous: bool):
        """
        增加积分
        :params num: 数量
        :params continuous: 是否为连续签到成功
        """
        cont = "continuous_sign_times"
        cont = f"{cont}={cont}+1" if continuous else f"{cont}=1"
        bot_db.update(f"{INFO_TABLE_NAME} set integral=integral+%s,"
                      f"sign_number_times=sign_number_times+1,{cont},"
                      f"sign_time=now() where qid=%s", [num, self.user_id])

    def _add_user(self):
        # 添加用户信息
        bot_db.insert(f"{INFO_TABLE_NAME} (qid,first_group) values (%s,%s)", [self.user_id, self.group_id])

    def _get_user_info(self) -> dict:
        """
        查看是否有该用户信息，如果没有则添加该用户然后进行一次递归
        :return 然后用户信息
        """
        user_info = bot_db.select_all(f"{INFO_TABLE_NAME} where qid=%s", [self.user_id])
        if user_info:
            return user_info[0]
        self._add_user()
        return self._get_user_info()


class SignIn(Methods):
    unit = INTEGRAL_UNIT
    name = INTEGRAL_NAME

    def __init__(self, user_id: int, group_id: int):
        self.user_id = user_id
        self.group_id = group_id
        self.merge = self.unit + self.name
        self.user_info = self._get_user_info()

    def interval_day(self, date_time: datetime = None) -> int:
        """
        返回距离今天的间隔
        0 今日已签到
        1 连续签到
        :return int 正整数
        """
        date_time = date_time or self.user_info["sign_time"]
        return (datetime.today().date() - date_time.date()).days

    def sign_in(self) -> str:
        """
        :return: str 返回签到是否成功的信息
        """
        number = ADD_INTEGRAL_NUMBER
        if self.user_info["sign_time"]:
            number = self.sign_in_full()
            if not number:
                return "您今天已经签到过了哟！"
        else:
            self.add_integral(number, True)
        self.user_info["sign_number_times"] += 1
        return (f"好啦好啦，给你签到啦！今日获得{number}{self.merge}"
                f"[{ADD_INTEGRAL_NUMBER}][连续{self.user_info['continuous_sign_times']}]")

    def sign_in_full(self) -> Union[int, None]:
        """
        :return int 签到成功所获得的 integral 数量
                none 签到失败
        """
        days = self.interval_day()
        if days:
            number, not_now = ADD_INTEGRAL_NUMBER, days == 1
            if not_now:
                number += self.user_info["continuous_sign_times"]
            else:
                self.user_info["continuous_sign_times"] = 0
            self.add_integral(number, not_now)
            return number

    def query_info(self) -> str:
        if self.user_info:
            return ("签到状态:{sign_time}签到\n"
                    "与您相识:{create_time}天\n"
                    "{name}:{integral}{unit}").format(
                sign_time='未'if self.interval_day(self.user_info['sign_time'])else'已',
                create_time=self.interval_day(self.user_info['create_time']),
                name=self.name, unit=self.unit,
                integral=self.user_info['integral'])
        return "您还未签到过呢！"
