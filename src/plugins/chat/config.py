from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    data_path = "data.json"

    class Config:
        extra = "ignore"
