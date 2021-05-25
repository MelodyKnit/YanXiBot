import os
from .config import Config
from aiofile import async_open
from nonebot.plugin import export
from yaml import load as yaml_load, FullLoader
from json import loads as json_load

export = export()
config = Config()
slash = "/" if "/" in __file__ else "\\"
path = os.path.dirname(__file__).split(slash)
path = path[:path.index(config.dir_name)]
file_types = {
    "json": json_load,
    "yml": lambda value: yaml_load(value, Loader=FullLoader)
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


def read_path(file_path: list) -> read_file:
    async def _read_file(file_name: str, file_type: str = None):
        value = await read_file(slash.join([*file_path, file_name]))
        if file_type is None:
            file_type = file_name.split(".")[-1]
        return file_types.get(file_type or "", lambda data: data)(value)
    return _read_file


# dir name
DATA_DIR_NAME = get_dir(config.data_dir_name)
CONFIG_DIR_NAME = get_dir(config.config_dir_name)
# export
export.read_data = read_path(DATA_DIR_NAME)
export.read_config = read_path(CONFIG_DIR_NAME)
