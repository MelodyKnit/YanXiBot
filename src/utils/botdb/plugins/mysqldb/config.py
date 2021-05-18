from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    file_path = "init/mysql_table.sql"

    class Config:
        extra = "ignore"
