# W2_PythonR4_Todolist_API

>## 项目说明
>
>- 用于西二python组四轮考核任务
>- 基于flask框架 Mysql数据库 Redis数据库
>- 注意！mysql未整合！
>- Todolist-API V1.0 2021.3.19-2021.4.11
>- © Mark Polo 2017-2021 All Right Reserved.

## 依赖相关

`pip install flask flask_sqlalchemy flask_migrate pymysql tornado`

redis 服务器，默认端口

mysql 服务器，默认端口，root -p 123456

## 用法&功能

- 基于REST的API路径设计
- 返回json格式的回报文，做出合理响应
- 最基本的跨域
- 增删查改，注册登录
- 基于token的身份认证，有效期可更改
- 基于redis的历史记录缓存
- 基于tornado&nginx的部署和负载平衡

## 本轮博客

### 概述

这轮做了一个todolist的API，基本上完成了规定的要求，但是也有一些遗憾，比如

- 跨域没有集成
- 用户功能不完善
- 没能做到uwsgi部署，安装报错

### 开发难点和解决

#### 跨域

本来是想用flask自带的一个cors模组，但是配置时候出了问题，导致它实际上不能接管视图的回报头。后来用手动调用

`@app.after_request`

这个修饰器去手动地为每一个回报头加cors字段。这样的坏处是不能对不同的报文做出不同反馈，不能很方便地配置。

未来还是打算用模组。

#### redis

了解到redis是一种key-value型的数据库。设计出key和value也是很重要的。

考虑到每个用户都有自己的历史记录，我把key设置成和用户id相关的

`history = 'history_%s' % userId`

value就有点问题。

我把value设成限长列表，其实就是先push再trim。

但是push的是字符串。字符串在进redis的value类型时会转成byte类型，导致它不能json化。

我的做法是构造一个新数组去存放decode之后的字符串。

```python
historyList = conn.lrange(history, 0 ,9)
listToOutput = list()
for obj in historyList:
 listToOutput.append(obj.decode())
```
