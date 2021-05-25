from typing import Iterable, Union
from .data_source import MySQLdbMethods
from typing import Union

format_keys = {
    "today": "now()"
}


def args_str(args: Iterable[str], or_to: str = "") -> str:
    return ",".join([str(i) for i in args]) if args else or_to


def kwargs_str(kws: dict) -> str:
    args = []
    for k in kws:
        if not isinstance(kws[k], (int, float)):
            args.append(f"{k}=\"{kws[k]}\"")
        else:
            args.append(f"{k}={str(kws[k])}")
    return ",".join(args)


def key_value(kws: dict):
    return args_str(kws.keys()), args_str(kws.values())


def where_str(where: Union[dict, str], or_to: str = "") -> str:
    if where:
        if isinstance(where, dict):
            where = kwargs_str(where)
        return "WHERE %s" % where
    return or_to


class SQLMethods(MySQLdbMethods):
    __slots__ = tuple()

    async def insert(self, __table: str, **kwargs):
        """
        :param __table: 表名
        :param kwargs:  需要添加的参数
        """
        keys, values = key_value(kwargs)
        sql = "INSERT INTO {table} ({keys}) VALUES ({values})".format(
            table=__table,
            keys=keys,
            values=values
        )
        await self.execute_commit(sql)

    async def update(self, __table: str, where: Union[dict, str] = None, **kwargs):
        """
        :param __table: 表名
        :param where: 规则
        :param kwargs:  需要更改的参数
        """
        sql = "UPDATE {table} SET {obj} {where}".format(
            table=__table,
            obj=kwargs_str(kwargs),
            where=where_str(where)
        )
        await self.execute_commit(sql)

    async def delete(self, __table: str, *args, where: Union[dict, str] = None):
        """
        :param __table: 表名
        :param args:    需要删除的那一列参数
        :param where: 规则
        """
        sql = "DELETE {args} FROM {table} {where}".format(
            args=args_str(args),
            table=__table,
            where=where_str(where)
        )
        await self.execute_commit(sql)

    async def select(self, __table: str, *args, where: Union[dict, str] = None) -> list:
        """
        :param __table: 表名
        :param args:    需要查找的参数
        :param where: 规则
        :return: list   返回信息列表
        """
        sql = "SELECT {args} FROM {table} {where}".format(
            table=__table,
            args=args_str(args, "*"),
            where=where_str(where)
        )
        await self.execute(sql)
        title = [next(i.__iter__()) for i in self.cur.description]
        return [{t: v for t, v in zip(title, r)} for r in self.fetchall().result()]
