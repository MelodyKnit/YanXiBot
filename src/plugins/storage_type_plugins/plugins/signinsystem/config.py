from pydantic import BaseSettings


class Config(BaseSettings):
    file_path = "sign_in.yml"
    # 回复消息是依照某类数据来定义的
    reply_basis = {
        "reply_true": "continuous",
        "reply_false": "repeats",
    }

    class Config:
        extra = "ignore"

