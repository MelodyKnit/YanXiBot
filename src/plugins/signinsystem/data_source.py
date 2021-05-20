from nonebot import require
from datetime import datetime
from yaml import load, FullLoader
from .config import Config


config = Config()
bot_db = require("botdb").BotDBMethods()
read_config = require("readfile").read_config


def get_days(__datetime: datetime, to_datetime: datetime = None) -> int:
    if __datetime:
        to_datetime = to_datetime if to_datetime else datetime.today()
        return (__datetime.date() - to_datetime.date()).days
    return 1


def is_month(__datetime: datetime, to_datetime: datetime = None) -> bool:
    """
    判断是否为本月
    """
    if __datetime:
        to_datetime = to_datetime if to_datetime else datetime.today()
        return __datetime.month == to_datetime.month
    return False


class GetUserInfo:
    table = "user_info"
    __slots__ = ("user_id", "group_id", "user_info", "_is_push", "config")

    def __init__(self, qid: int, gid: int = 0):
        self.user_id = qid
        self.group_id = gid or 0
        self.user_info = {}
        self._is_push = False
        self.config = {}

    async def __user_info(self):
        user_info = await bot_db.select(self.table, where={"qid": self.user_id})
        if not user_info:
            await bot_db.insert(self.table, qid=self.user_id, sign_group=self.group_id)
            return await self.__user_info()
        return user_info[0]

    async def __aenter__(self):
        self.user_info = await self.__user_info()
        self.config = load(await read_config(config.file_path), Loader=FullLoader)
        return self

    async def __aexit__(self, *args):
        if self._is_push:
            await bot_db.update(self.table, **self.user_info, where={"qid": self.user_id})


class SetUserInfo(GetUserInfo):
    __slots__ = ()

    def _set_frequency(self) -> bool:
        """
        对签到次数，连续签到，本月签到进行递增

        :returns:
            查看是否满足签到条件
            如果满足则进行对次数增加并且返回True
        """
        days = get_days(self.user_info["sign_time"])
        if days:
            # 重置连续与月签次数
            if days != -1:
                self.user_info["continuous"] = 0
            if not is_month(self.user_info["sign_time"]):
                self.user_info["month_signs"] = 0
            # 进行递增
            self.user_info["month_signs"] += 1
            self.user_info["continuous"] += 1
            self.user_info["signs"] += 1
            self.user_info["repeats"] = 0
            return True
        # 重复签到递增
        else:
            self.user_info["repeats"] += 1
        return False

    def _set_integral(self) -> int:
        """
        :详细:
        设置增加integral的数量
        初始增加数量 + 连续签到最大天数以内的天数 * 连续签到所加的数量

        :returns:
            共计增加的数量
        """
        # 判断是否超出最大天数，如果超出则选择最大天数
        num = self.config["integral"] + min(
            self.user_info["continuous"], self.config["continuous"]["max_day"]
        ) * self.config["continuous"]["increase"]
        self.user_info["integral"] += num
        return num

    def _format_reply(self, text: str, more: dict = None) -> str:
        more = more or {}
        return text.format(
            name=self.config["integral_type"]["name"],
            unit=self.config["integral_type"]["unit"],
            **self.user_info,
            **more
        )

    def _reply_msg(self, __type: str) -> str:
        # 获取回复消息
        msgs = self.config[__type]
        # 用户信息里面抽取回复消息对应数据库的某项数据，然后与消息数量做取值，取最小值
        __type = min(self.user_info[config.reply_basis[__type]], len(msgs) - 1)
        return msgs[__type]


class SignIn(SetUserInfo):
    __slots__ = ()

    def sign_in(self):
        self._is_push = True
        if self._set_frequency():
            self.user_info["sign_group"] = self.group_id
            self.user_info["sign_time"] = datetime.today()
            return self._format_reply(self._reply_msg("reply_true"), {
                "get_integral": self._set_integral()
            })
        return self._format_reply(self._reply_msg("reply_false"))

    def query(self) -> str:
        msg = [self._format_reply(txt, {
            "is_day_login": "未签到" if get_days(self.user_info["sign_time"]) else "已签到",
            "meets": -get_days(self.user_info["create_time"])
        }) for txt in self.config["reply_query"]]
        num = int(max([len(i.encode("gbk")) for i in msg]) * 1.8)
        msg = "\n".join(msg)
        return f"┌{' ' * num}┐\n{msg}\n└{' ' * num}┘"


