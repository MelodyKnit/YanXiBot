# 机器人数据库
为后期实现签到、商店、好感度等系统所编写的的数据库

## 数据库类型
- [x] MySQL数据库
- [ ] 文件数据库

机器人数据库会去与MySQL数据库建立连接，如果连接失败则会自动启用文件数据库进行存储数据，会将数据写入在[data/botdb](../../../data)文件夹下(目前暂未编写文件数据库)

MySQL总是连接失败但命令行可以连接

use mysql
<br>
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';