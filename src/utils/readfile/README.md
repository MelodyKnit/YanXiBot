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
```
读取后会返回文件数据
```python
await read_data("file")
```

## 特性
read_json与read_data具备区分文件后缀的文件类型然后进行load

目前支持.json与.yml后缀

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
print(value[0]["name"])
```
可以用如上写法

若不想使用该特性可以在函数后面加上False参数
```python
value = await read_config("user.json", False)
print(value)
# print(value[0]["name"]) 会报错
```

