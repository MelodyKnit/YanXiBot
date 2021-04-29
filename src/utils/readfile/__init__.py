import os
from .config import *
from json import loads

slash = "/" if "/" in __file__ else "\\"
path = os.path.dirname(__file__).split(slash)
path = path[:path.index(DIR_NAME)]


def get_test_dir(args: list, dir_name: str) -> list:
    """
    辨别是否是测试目录 __目录__ 带双下划线的目录为编写时候的测试目录
    :param args:  list 目录需要为拆分为 list
    :param dir_name: 目录名
    :return: 返回拼接后的目录
    """
    if not os.path.isdir(slash.join([*args, f"__{dir_name}__"])):
        return [*args, dir_name]
    return [*args, f"__{dir_name}__"]


def read_file(file_path):
    try:
        with open(file_path, mode="r") as file:
            return loads(file.read())
    except FileNotFoundError:
        return None


def read_data(file_name: str) -> dict:
    return read_file(slash.join([*DATA_DIR_NAME, file_name]))


def read_config(file_name: str) -> dict:
    return read_file(slash.join([*CONFIG_DIR_NAME, file_name]))


DATA_DIR_NAME = get_test_dir(path, DATA_DIR_NAME)
CONFIG_DIR_NAME = get_test_dir(path, CONFIG_DIR_NAME)
