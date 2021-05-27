import os
from .config import Config
from aiofile import async_open
from nonebot.plugin import export
from yaml import load as yaml_load, FullLoader
from json import (loads as json_load, dumps as json_dump)

export = export()
config = Config()
slash = "/" if "/" in __file__ else "\\"
path = os.path.dirname(__file__).split(slash)
path = path[:path.index(config.dir_name)]
read_types = {
    "json": json_load,
    "yml": lambda value: yaml_load(value, Loader=FullLoader)
}
read_types["yaml"] = read_types["yml"]

write_types = {
    "json": lambda value: json_dump(value, ensure_ascii=False)
}


def get_dir(dir_name: str) -> list:
    """
    辨别是否是测试目录 __目录__ 带双下划线的目录为编写时候的测试目录
    :param dir_name: 目录名
    :return: 返回拼接后的目录
    """
    if not os.path.isdir(slash.join([*path, f"__{dir_name}__"])):
        return [*path, dir_name]
    return [*path, f"__{dir_name}__"]


async def read_file(file_path: str):
    try:
        async with async_open(file_path, mode="r") as file:
            return await file.read()
    except FileNotFoundError:
        return None


async def write_file(file_path: str, value, mode="w"):
    async with async_open(file_path, mode=mode) as file:
        await file.write(value)


def read_path(file_path: list) -> read_file:
    async def _read_file(file_name: str, file_type: str = None):
        value = await read_file(slash.join([*file_path, file_name]))
        if file_type is None:
            file_type = file_name.split(".")[-1]
        return read_types.get(file_type or "", lambda data: data)(value)
    return _read_file


def write_path(file_path: list, mode="w") -> read_file:
    """
    判断文件类型是否有输入
        如果未输入到则提取后缀
    判断是否不是字符串或字节数据
        不是则将文件进行
    """
    async def _write_file(file_name: str, value, file_type: str = None):
        if file_type is None:
            file_type = file_name.split(".")[-1]
        if not isinstance(value, (str, bytes)):
            value = write_types.get(file_type or "", lambda data: str(data))(value)
        await write_file(slash.join([*file_path, file_name]), value, mode)
    return _write_file


# dir name
DATA_DIR_NAME = get_dir(config.data_dir_name)
CONFIG_DIR_NAME = get_dir(config.config_dir_name)
# export
export.read_data = read_path(DATA_DIR_NAME)
export.read_config = read_path(CONFIG_DIR_NAME)
export.write_data = write_path(DATA_DIR_NAME)
export.write_config = write_path(CONFIG_DIR_NAME)
