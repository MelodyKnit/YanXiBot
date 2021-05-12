from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    dir_name = "src"
    data_dir_name = "data"
    config_dir_name = "config"

    class Config:
        extra = "ignore"


DIR_NAME = "src"
DATA_DIR_NAME = "data"
CONFIG_DIR_NAME = "config"
