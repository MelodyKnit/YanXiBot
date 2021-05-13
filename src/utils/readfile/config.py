from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    dir_name = "src"
    data_dir_name = "data"
    config_dir_name = "config"

    class Config:
        extra = "ignore"
