# 机器人数据库

通过run函数运行将MySQLDB实列传入到DBMethods.db

操作数据库时可以调用 get_bot_db 返回DBMethods实列来操作数据库增删改查

```python
from nonebot.plugin import require

require = require("botdb")
bot_db = require.get_bot_db(True)
bot_db.select(f"* from {require.info_table}")
```