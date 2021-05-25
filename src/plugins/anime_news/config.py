from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    main_url = "http://www.yhdm.so/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }

    class Config:
        extra = "ignore"
