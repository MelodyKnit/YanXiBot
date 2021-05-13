# WeCome

对群成员加入与退出做出相应回复

## 配置
对于群员加入与退出请参考：[wecome](../../config/wecome.yml)

## 格式化字符
可在[wecome](../../config/wecome.yml)回复消息时加入格式字符<br>
如：{at}欢迎{name}加入本群
<div>
<table>
    <thead>
        <tr>
            <td colspan="2" align="center">IncreaseMessage</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>uid</td>
            <td>用户的QQ号</td>
        </tr>
        <tr>
            <td>gid</td>
            <td>本群群号</td>
        </tr>
        <tr>
            <td>oid</td>
            <td>处理人id</td>
        </tr>
        <tr>
            <td>time</td>
            <td>入群时间</td>
        </tr>
        <tr>
            <td>name</td>
            <td>用户名</td>
        </tr>
        <tr>
            <td>sex</td>
            <td>用户性别</td>
        </tr>
        <tr>
            <td>at</td>
            <td>at用户</td>
        </tr>
    </tbody>
</table>
<table align="center">
    <thead>
        <tr>
            <td colspan="2" align="center">DecreaseMessage</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>uid</td>
            <td>用户的QQ号</td>
        </tr>
        <tr>
            <td>gid</td>
            <td>本群群号</td>
        </tr>
        <tr>
            <td>oid</td>
            <td>处理人id（自己退出则会为0）</td>
        </tr>
        <tr>
            <td>time</td>
            <td>退出时间</td>
        </tr>
        <tr>
    </tbody>
</table>
</div>
