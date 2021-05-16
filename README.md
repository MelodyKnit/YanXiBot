<h1 align="center">YanXiBot</h1>
<p align="center">基于Nonebot2编写与gocq实现的QQ机器人程序</p>

<div align="center">
<img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
<img src="https://img.shields.io/badge/nonebot2-red" alt="nonebot">
<br/>
</div>

<h3 align="center">该项目还属于扩展阶段，会加入更多实用性高的插件，敬请期待</h3>

## 部署
```shell
git close https://www.github.com/melodyknit/YanXiBot
cd YanXiBot
pip install -r requirements.txt
nb run
```

## 配置
配置项参考 [.env 文件](./.env)

## 实现功能

- [x] [聊天](src/plugins/chat)
- [x] [获取动漫资源](src/plugins/animeres)
- [x] [签到系统](src/plugins)
- [x] [加入/退出群词](src/plugins/wecome)

## 预计新增

- [ ] BiliBili投稿视频信息
- [ ] BiliBili番剧动态
- [ ] 动漫图片识别
- [ ] 番剧图片识别
- [ ] 好感度系统
- [ ] 养成系统
- [ ] 商店系统
