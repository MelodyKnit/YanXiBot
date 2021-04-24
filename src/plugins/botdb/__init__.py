from .data_source import DBMethods


class BotMethods(DBMethods):
    """
    机器人操作数据库的方法
    """
    def add_user_init_info(self, qid: int, gid: int):
        self.insert(f"{self.INFO_TABLE_NAME} "
                    f"(qid,first_group) values "
                    f"(%s,%s)", [qid, gid])


class BotDB(BotMethods):
    __slots__ = ()

    def init(self):
        self.create_user_info_table()

