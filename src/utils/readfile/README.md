# Read File
<b>会以json格式读取src同级目录的data与config文件夹中的文件</b>

<pre>
<code>
├─config
│  └─file
├─data
│  └─file
└─src
</code>
</pre>

```python
from nonebot.plugin import export
export = export("readfile")
read_data = export.read_data
read_config = export.read_config
write_data = export.write_data
write_config = export.write_config
```
读取后会返回文件数据
```python
await read_data("file")
```

## 特性
read_json与read_data具备区分文件后缀的文件类型然后进行load

目前支持.json与.yml后缀

### 读取

```json
[
  {
    "name": "bob",
    "sex": "man"
  }
]
```
例如读取如上json文件假设名为user.json
```python
value = await read_config("user.json")
# 或者 value = await read_config("user.json", file_type="json")
print(value[0]["name"])
```
可以用如上写法

若不想使用该特性可以在函数后面加上False参数
```python
value = await read_config("user.json", file_type=False)
print(value)
# print(value[0]["name"]) 会报错
```
### 写入

```json

```
一个空文件，假设名为user.json，我需要将它保存在data目录下

```python
user_list = [{
    "name": "bob",
    "sex": 18,
    "chinese name": "鲍勃"
}]
await write_data("user.json", user_list)
```
```json
[{"name": "bob", "sex": 15, "chinese name": "鲍勃"}]
```
与读取一样，不想使用特性可以传入file_type=false

## 分别支持

| read_file | write_file |
| :-----| :---- |
| json | json |
| yaml |  |