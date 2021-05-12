from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    info_table_name: str = "user_info"

    class Config:
        extra = "ignore"
