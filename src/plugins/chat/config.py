from pydantic import BaseSettings
from pprint import pprint


class Config(BaseSettings):
    # Your Config Here
    driver: str = None

    class Config:
        extra = "ignore"
