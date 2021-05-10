# Read File
<b>会以json格式读取src同级目录的data与config文件夹中的文件</b>

<pre>
<code>
├─config
│  └─files.json
├─data
│  └─files.json
└─src
</code>
</pre>

```python
from nonebot.plugin import export
export = export("readfile")
read_data = export.read_data
read_config = export.read_config
```
读取后会返回dict
```python
read_data("file.json")
```
