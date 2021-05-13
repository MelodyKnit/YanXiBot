from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    file_path = "wecome.yml"

    class Config:
        extra = "ignore"
