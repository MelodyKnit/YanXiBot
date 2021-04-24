from .data_source import MySQLdb
from pymysql.err import IntegrityError


class DBMethods(MySQLdb):
    """
    集成在数据库的一些方法
    """
    def create_user_info_table(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self.INFO_TABLE_NAME}("
               "qid BIGINT PRIMARY KEY COMMENT '用户QQid',"
               "first_group BIGINT NOT NULL COMMENT '第一次注册所在群',"
               "nickname VARCHAR(16) COMMENT '用户名称',"
               "create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间'"
               ")")
        self.execute(sql)

    def insert(self, query: str, args=None):
        try:
            self.execute(f"insert into {query}", args)
            self.database.commit()
        except IntegrityError:
            self.database.rollback()

    def select(self, query: str, args=None):
        self.execute(f"select {query}", args)
        return self.cursor.fetchall()

# print(os.getcwd())
# pprint(os.getenv("PATH"))


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

