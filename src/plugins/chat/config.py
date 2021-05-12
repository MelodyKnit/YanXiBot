from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    driver: str = None

    class Config:
        extra = "ignore"
