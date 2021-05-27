from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    news_send_time = 7
    news_recipient_filename = "news_recipient.json"
    # 动漫新闻发送时间
    main_url = "http://www.yhdm.so/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }

    class Config:
        extra = "ignore"

    class SendInfo:
        __slots__ = ("api", "id_type", "id_list", "send_list", "news_list", "remove")

        def __init__(self, info: dict):
            self.api: str = info["api"]
            # 未发现该好友或群则删除该id
            self.remove = info["remove"]
            # 发送消息的类型，如group_id或user_id
            self.id_type: str = info["id_type"]
            # 好友列表或群列表
            self.id_list: list = info["id_list"]
            # 需要发送的群列表或好友
            self.send_list: list = info["send_list"]
            # 全部新闻
            self.news_list: list = info["news_list"]

